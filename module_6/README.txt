Name: Harry Ma (hm41)

Module Info: Module 5 - Software Assurance + Secure SQL (Due: 02/23/26 11:59PM ET)

Approach: 
Software Assurance & CI/CD: The primary focus of this module was "shifting left" on security. 
A GitHub Actions pipeline was implemented to enforce code quality and security standards before 
any code is merged. This includes a strict Pylint gate requiring a 10/10 score and automated 
Snyk scans to detect vulnerabilities in the dependency tree.
HOW TO Run Pylint: 
In Terminal - cd to module_5 folder -> run 'pylint src/' 

SQL Injection Defense: The entire database interaction layer was refactored to eliminate unsafe 
string formatting. Using psycopg SQL composition (sql.SQL, sql.Identifier, and sql.Placeholder), 
dynamic components like table names are safely quoted and user-supplied values are handled via 
server-side parameter binding. Additionally, an inherent LIMIT was applied to all queries to 
prevent mass data exfiltration.

Dependency Management: To improve reproducibility, the project transitioned to a robust packaging 
structure with the addition of a setup.py file. This defines package metadata and requirements 
clearly. Furthermore, pydeps and Graphviz were integrated into the workflow to generate a visual 
dependency graph (dependency.svg), ensuring the architecture remains clean and free of circular 
dependencies.

Least-Privilege Database Design: The connection strategy was hardened by removing all hard-coded 
credentials in favor of environment variables. A dedicated, non-superuser database account was 
configured with the minimum necessary permissions—specifically SELECT and INSERT on required 
tables—adhering strictly to the principle of least privilege.

Automated Visualization: The CI pipeline was configured to automatically generate the dependency.svg 
file on every push. This ensures that the documentation of the system's internal structure stays 
synchronized with the actual codebase, providing immediate feedback on how new libraries affect the 
overall project footprint.

How to Run: 
1. Initialize postgreSQL locally 
2. Install requirements.text
3. Run python3 -m pytest for coverage 
4. Access documentation via Read the Doc- https://jhu-software-concepts-hma41.readthedocs.io/en/latest/

Fresh Install:
1) pip
In Terminal:
python -m venv venv 
source venv/bin/activate (Mac) OR venv\Scripts\activate
pip install -r requirements.txt
pip install -e

2) uv 
In Terminal:
uv venv
source .venv/bin/activate 
uv pip sync requirements.txt
uv pip install -e

Known Bugs/Workarounds: 
To achieve a 10/10 Pylint rating and a successful CI/CD pass, the following configurations were applied: 
Minor stylistic and non-functional linting rules were suppressed in the .pylintrc file where they did not 
impact application performance or logic. Additionally, diskcache was explicitly ignored in the .snyk 
policy file; while it remains necessary for the LLM component’s functionality, it currently lacks the 
support metadata required for a standard Snyk vulnerability scan, making it a known and accepted dependency risk.
