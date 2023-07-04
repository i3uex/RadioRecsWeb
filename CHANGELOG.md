# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Requirements.

### Changed

- Use relative URLs.

## [0.0.5] - 2019-07-24

### Added

- Show CSV formatted as table.
- Download all transformed datasets as ZIP file.
- Transformed dataset are stored in a different folder each session.

## [0.0.4] - 2019-07-10

### Added

- Code comments.

### Fixed

- Squashed various bugs.

## [0.0.3] - 2019-07-09

### Added

- Improved user interface.

## [0.0.2] - 2019-07-07

### Added

- Reduce dimensionality transformations unit tests.
- Reduce dimensionality transformations implementation.
- Minimal reduce dimensionality test datasets.
- Feature selection transformations unit tests.
- Feature selection transformations implementation.
- Minimal feature selection test datasets.
- Feature engineering transformations unit tests.
- Feature engineering transformations implementation.
- Minimal feature engineering test datasets.
- Scale/normalize transformations unit tests.
- Scale/normalize transformations implementation.
- Minimal scale/normalize test dataset.
- Encoding transformations unit tests.
- Encoding transformations implementation.
- Minimal encoding test dataset.

## [0.0.1] - 2019-06-28

### Added

- Error reporting via HTML alerts, from Python exception handlers to HTTP 500.
- Missing values transformations unit tests.
- Missing values transformations implementation.
- Minimal test dataset.
- Log debug information to file **debug.log** inside **log** folder.
- Common access strategy to transformation execution.
- Factory to access transformers.
- Transformers for each transformation category.
- Mechanism to get transformation enumeration from its string.
- Transformations as custom enumerations.
