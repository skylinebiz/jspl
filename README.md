### JSPL

Custom Frappe/ERPNext app for JSPL, currently featuring **Blanket Booking Order**: an item-group-level companion to ERPNext's Blanket Order that commits quantities against an Item Group (instead of a specific Item Code) for a customer or supplier, and tracks consumption automatically as linked Purchase Orders are submitted or cancelled.

### Release Notes

- [release.md](release.md) — the latest release announcement.
- [CHANGELOG.md](CHANGELOG.md) — full version history: what was added, changed, updated, and removed in each release.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app jspl
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/jspl
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
