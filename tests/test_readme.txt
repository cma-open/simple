Test structure by test type

a_unit
    tests with subdirectories to match package subdirectories
    these tests do not create or modify data

b_integration
    selected integration tests by topic area
    these tests do not create or modify data

c_end_to_end
    selected end-to-end tests for key parts of the system
    some of these tests will create or modify data on disk

d_user_interface
    tests for the main user editable or configurable parts of the system
    some of these tests will create or modify data on disk
