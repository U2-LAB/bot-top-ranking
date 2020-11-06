#!/bin/bash
coverage run -m unittest -v unittests.test_handlers.TestHandlers unittests.test_help_functions.TestHelpFunctions unittests.test_work_with_csv.TestWorkWithCsv unittests.test_decorators.TestDecorators
coverage report
