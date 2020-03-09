# hash-app-tester
Hash app tester written in Python

1. Clone the repo

     git clone https://github.com/jzhang88/hash-app-tester.git
 
 2. Run the automated test cases
  - From IDE, select individual test suite under tests folder and run as Python-Run or Python unit_test
  - From IDE, select the tests folder and run as Python unit_test
  
  3. Version tested
  
      hash app: 0c3d817
      python: 3.5.2

   4. Python module required
   - requests
   - aiohttp
   - hashlib
   - jsonschema

   5. Testing Scope
   - Verify status code and response of all the supported requests
   - Verify proper error message is returned for invalid requests
   - Verify unsupported requests are rejected with correct status code and error message
   - Verify simultaneous requets can be handled peroperly to meet certain performance requirement
   
   6. List of test cases
   - List of test cases can be found in /docs/testcases
   - automated tests can be found under /tests
   
   7. Sample execution output
   - A sample of execution output can be found at /docs/sample_output_of_test_executions
   
   8. Utility files
   - Base functions to send CRUD requests can be found in /lib/hashing_crud.py
   - Password generations and String Hashing functions can be found in /lib/string_hash_utils.py
   
   9. Schemas
   - JSON schema used to verify stats reponse can be found in /schema/hash_stats.json
   
   10. Defects found
   - List of defects can be found in /docs/defects

