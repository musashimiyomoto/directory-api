#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[1;35m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}==============================================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}==============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_poetry() {
    if ! command -v poetry &> /dev/null; then
        print_error "Poetry is not installed. Please install Poetry to continue."
        exit 1
    fi
}

install_dependencies() {
    print_header "INSTALLING DEPENDENCIES"
    pip install --upgrade pip
    pip install poetry
    poetry shell
    poetry install --with dev,test
    poetry run pre-commit install
    print_success "Dependencies installed successfully"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker to continue."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose to continue."
        exit 1
    fi
}

check_alembic() {
    if ! poetry run alembic --help &> /dev/null; then
        print_error "Alembic is not available. Make sure dependencies are installed."
        exit 1
    fi
}

load_env() {
    if [ -f .env ]; then
        set -a
        source .env
        set +a
        print_info "Loaded environment variables from .env"
    fi
}

setup_local_env() {
    if [ ! -f .env ]; then
        print_error ".env file not found. Please create it from .env.example"
        exit 1
    fi

    cp .env .env.backup
    print_info "Created backup of .env file"

    sed -i 's/DB_HOST=db/DB_HOST=localhost/g' .env
    print_success "Updated DB_HOST to localhost in .env"

    load_env
}

restore_env() {
    if [ -f .env.backup ]; then
        mv .env.backup .env
        print_success "Restored original .env file"
    else
        print_warning "No backup file found, manually restoring DB_HOST"
        sed -i 's/DB_HOST=localhost/DB_HOST=db/g' .env
        print_success "Restored DB_HOST to db in .env"
    fi
}

cleanup() {
    print_warning "Script interrupted, restoring .env file..."
    restore_env
    exit 1
}

trap cleanup INT TERM

format_code() {
    print_header "CODE FORMATTING"

    print_warning "Running isort..."
    if poetry run isort .; then
        print_success "isort completed successfully"
    else
        print_error "Error running isort"
        return 1
    fi

    print_warning "Running black..."
    if poetry run black .; then
        print_success "black completed successfully"
    else
        print_error "Error running black"
        return 1
    fi

    print_success "Code formatting completed"
}

check_lint() {
    print_header "CHECKING CODE LINT"
    if poetry run ruff check .; then
        print_success "ruff check completed successfully"
    else
        print_error "Error running ruff check"
        return 1
    fi

    if poetry run pyright .; then
        print_success "pyright completed successfully"
    else
        print_error "Error running pyright"
        return 1
    fi

    print_success "Code lint check completed"
}

check_formatting() {
    print_header "CHECKING CODE FORMATTING"

    print_warning "Running check black..."
    if poetry run black --check --diff .; then
        print_success "black check completed successfully"
    else
        print_error "Error running black check"
        return 1
    fi

    print_warning "Running check isort..."
    if poetry run isort --check-only --diff .; then
        print_success "isort check completed successfully"
    else
        print_error "Error running isort check"
        return 1
    fi

    print_success "Code formatting check completed"
}

run_tests() {
    print_header "RUNNING TESTS"

    print_warning "Running pytest..."
    if poetry run pytest -v --cov=. --cov-report=term-missing --cov-report=xml; then
        print_success "All tests passed successfully"
    else
        print_error "Some tests failed"
        return 1
    fi
}

build_docker() {
    print_header "DOCKER COMPOSE BUILD"

    print_warning "Starting containers..."
    if docker-compose up -d --build; then
        print_success "Containers started successfully"
        echo ""
        print_warning "Container status:"
        docker-compose ps
        echo ""
        print_success "API available at: http://localhost:8000"
        print_success "DB UI available at: http://localhost:8080"
    else
        print_error "Error starting containers"
        return 1
    fi
}

generate_migration() {
    local message="$1"
    if [ -z "$message" ]; then
        print_error "Migration message is required"
        echo "Usage: $0 migrate generate \"your migration message\""
        exit 1
    fi

    print_header "GENERATING MIGRATION"
    print_info "Generating new migration: $message"
    setup_local_env

    if poetry run alembic revision --autogenerate -m "$message"; then
        print_success "Migration generated successfully"
    else
        print_error "Failed to generate migration"
        restore_env
        exit 1
    fi

    restore_env
}

upgrade_migrations() {
    print_header "UPGRADING MIGRATIONS"
    setup_local_env

    if poetry run alembic upgrade head; then
        print_success "Migrations upgraded successfully"
    else
        print_error "Failed to upgrade migrations"
        restore_env
        exit 1
    fi

    restore_env
}

downgrade_migrations() {
    local target="${1:-1}"
    print_header "DOWNGRADING MIGRATIONS"
    print_info "Downgrading to: $target"
    setup_local_env

    if poetry run alembic downgrade "$target"; then
        print_success "Migrations downgraded successfully"
    else
        print_error "Failed to downgrade migrations"
        restore_env
        exit 1
    fi

    restore_env
}

show_migration_history() {
    print_header "MIGRATION HISTORY"
    setup_local_env

    poetry run alembic history

    restore_env
}

show_current_migration() {
    print_header "CURRENT MIGRATION"
    setup_local_env

    poetry run alembic current

    restore_env
}

show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Development Commands:"
    echo "  install             Install dependencies"
    echo "  format              Format code using isort and black"
    echo "  check               Check code formatting and lint"
    echo "  test                Run tests"
    echo "  build               Build and run Docker Compose"
    echo "  all                 Execute all operations (format + test + build)"
    echo ""
    echo "Migration Commands:"
    echo "  migrate generate \"message\"  Generate new migration with message"
    echo "  migrate upgrade               Apply all pending migrations"
    echo "  migrate downgrade [target]    Rollback migrations (default: -1)"
    echo "  migrate history               Show migration history"
    echo "  migrate current               Show current migration"
    echo ""
    echo "Examples:"
    echo "  $0 format"
    echo "  $0 test"
    echo "  $0 build"
    echo "  $0 all"
    echo "  $0 migrate generate \"Add user table\""
    echo "  $0 migrate upgrade"
    echo "  $0 migrate downgrade"
    echo "  $0 migrate downgrade base"
}

main() {
    case "${1:-all}" in
        install)
            install_dependencies
            check_poetry
            ;;
        format)
            check_poetry
            format_code
            ;;
        check)
            check_poetry
            check_formatting
            check_lint
            ;;
        test)
            check_poetry
            run_tests
            ;;
        build)
            check_docker
            build_docker
            ;;
        all)
            check_poetry
            check_docker

            print_header "FULL DEVELOPMENT CYCLE"

            if install_dependencies && format_code && check_lint && run_tests && build_docker; then
                print_success "All operations completed successfully!"
            else
                print_error "Some operations failed"
                exit 1
            fi
            ;;
        migrate)
            check_poetry
            check_alembic

            case "${2:-help}" in
                generate)
                    generate_migration "$3"
                    ;;
                upgrade)
                    upgrade_migrations
                    ;;
                downgrade)
                    downgrade_migrations "$3"
                    ;;
                history)
                    show_migration_history
                    ;;
                current)
                    show_current_migration
                    ;;
            esac
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
