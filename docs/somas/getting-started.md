# Getting Started with SOMAS

This guide will walk you through creating your first project with SOMAS, the autonomous AI development pipeline.

---

## Prerequisites

Before you begin, ensure you have:
- Access to this GitHub repository
- Permission to create issues and PRs
- Basic understanding of Git and GitHub

No local setup required! SOMAS runs entirely on GitHub.

---

## Your First Project: A Simple Calculator CLI

Let's create a command-line calculator as our first SOMAS project.

### Step 1: Create the Issue

1. **Navigate to Issues**
   - Go to the [Issues tab](../../issues)
   - Click "New Issue"

2. **Select Template**
   - Choose "🤖 SOMAS Project Request"

3. **Fill in Project Details**

   **Title**: `[SOMAS] Calculator CLI Tool`

   **Project Idea**:
   ```
   Create a command-line calculator that can perform basic arithmetic operations.
   
   Features:
   - Support for addition, subtraction, multiplication, and division
   - Handle floating-point numbers
   - Provide clear error messages for invalid inputs
   - Support both interactive mode and direct calculation mode
   - Show usage help with --help flag
   ```

   **Project Type**: `CLI (Command-line tool)`

   **Preferred Programming Language**: `Python` (or your choice)

   **Technical Constraints**:
   ```
   - Must handle division by zero gracefully
   - Should validate numeric inputs
   - Must include comprehensive tests
   - Follow PEP 8 style guide (if Python)
   ```

4. **Submit the Issue**
   - Click "Submit new issue"
   - Note the issue number (e.g., #123)

---

### Step 2: Start the Pipeline

1. **Add the Trigger Label**
   - On your newly created issue, add the label: `somas-project`
   - You can add labels from the right sidebar

2. **Watch the Magic Begin**
   - Within moments, the GitHub Actions workflow will trigger
   - A new feature branch will be created: `somas/123`
   - A draft PR will be created and linked to your issue

---

### Step 3: Monitor Progress

The pipeline will progress through 7 stages autonomously. You can monitor progress in:

#### The Issue
Updates will be posted as comments by agents as they work:
```
🎯 Stage 1: Ideation
Agent: @somas-planner
Status: In Progress
Analyzing requirements and creating project plan...
```

#### The Pull Request
The PR will be created automatically in Stage 7 (Staging) with:
```
### Pipeline Stages

- [x] Ideation - Requirements analysis and planning
- [x] Specification - Complete specification document
- [x] Simulation - Monte Carlo optimization
- [x] Architecture - System design and component definition
- [x] Implementation - Code generation and testing
- [x] Validation - Quality assurance and security review
- [ ] Staging - PR creation and merge preparation (Human approval required)
```

#### GitHub Actions
- Go to the "Actions" tab to see workflow runs
- Click on the running workflow for detailed logs
- Each stage's output is logged

---

### Step 4: Watch the Agents Work

The pipeline runs autonomously through all 7 stages:

#### Stage 1: Ideation (5-10 minutes)
The **Planner** agent (GPT-5.2) will:
- Analyze your requirements
- Define the calculator's scope
- Break down into tasks (parser, calculator logic, CLI interface, tests)
- Create a project roadmap

**Output**: `.somas/projects/project-{issue-number}/artifacts/initial_plan.md`

#### Stage 2: Specification (15-30 minutes)
The **Specifier** agent (Claude Sonnet 4.5) will:
- Create complete SPEC.md document
- Define functional and non-functional requirements
- Document user stories with acceptance criteria
- Specify API contracts

**Output**: `SPEC.md`, `requirements.yml`
**Note**: This stage is now autonomous (no human approval needed)

#### Stage 3: Simulation (10-15 minutes)
The **Simulator** agent (Claude Sonnet 4.5) will:
- Run Monte Carlo simulations
- Identify optimal task execution sequence
- Determine critical path
- Maximize parallelization

**Output**: `execution_plan.yml`

#### Stage 4: Architecture (30-60 minutes)
The **Architect** agent (Claude Opus 4.5) will:
- Design system architecture
- Define components and interactions
- Create data models and API specs
- Document architectural decisions

**Output**: `ARCHITECTURE.md`, `api_specs.yml`, `data_models.yml`

#### Stage 5: Implementation (2-4 hours for this calculator)
The **Implementer** agent (Claude Sonnet 4.5) will:
- Generate production-ready code
- Create comprehensive test suites
- Perform security scanning
- Document code and APIs

**Output**: Source code, tests, docs in project directory

#### Stage 6: Validation (30-90 minutes)
The **Validator** agent verifies quality (with auto-retry on failure):
- Runs all tests, verifies coverage
- Performs code quality review
- Executes security scan
- Applies fixes and re-validates if needed

**Auto-retry**: Up to 3 attempts before human escalation
**Output**: `validation_report.json`, test results

#### Stage 7: Staging (Auto or Human Approval)
Final stage creates the PR:
- **Deployer** (Claude Opus 4.5): Prepares merge and deployment
- Creates pull request automatically
- **Dev environment**: Auto-merges after all checks pass
- **Prod environment**: Human approval required

**Output**: Pull request with all artifacts ready for review/merge

---

### Step 5: Review the Generated Code

When the staging stage completes, you'll be notified with a comment like:

```
🎉 SOMAS Pipeline Complete!

All stages have been completed successfully.

@scotlaclair - Please review the generated code and approve if ready to merge.
```

#### Review Checklist

1. **Check the README**
   - Is the project well-documented?
   - Are installation instructions clear?
   - Are usage examples provided?

2. **Review the Code**
   - Does it meet your requirements?
   - Is it well-structured and readable?
   - Is error handling appropriate?

3. **Check the Tests**
   - Are there comprehensive tests?
   - Does coverage meet 80%+ threshold?
   - Do all tests pass?

4. **Test the Functionality**
   - Clone the branch locally (optional)
   - Run the calculator
   - Test with various inputs
   - Verify error handling

#### Example Review

Navigate to the PR and review files:

**Files to Review**:
- `README.md` - Documentation
- `calculator.py` (or similar) - Main implementation
- `test_calculator.py` - Test suite
- `requirements.txt` or similar - Dependencies

**Check the Calculator Works**:
```bash
# Clone the branch (optional)
git checkout somas/123

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the calculator
python calculator.py --help
python calculator.py add 5 3
python calculator.py divide 10 2

# Run tests
pytest
```

---

### Step 6: Approve and Merge

If you're satisfied with the generated code:

1. **Approve the PR**
   - Click "Review changes"
   - Select "Approve"
   - Add optional comment
   - Submit review

2. **Mark as Ready**
   - The PR should already be marked as ready for review
   - If not, click "Ready for review"

3. **Merge**
   - Click "Merge pull request"
   - Confirm the merge
   - Optionally delete the branch

**Congratulations!** You've just created a complete CLI calculator using SOMAS! 🎉

---

### Step 7: Use Your New Tool

After merging, you can use your new calculator:

```bash
# Clone/pull the repository
git pull origin main

# Use the calculator
python calculator.py add 10 5
# Output: 15.0

python calculator.py multiply 7 8
# Output: 56.0

python calculator.py divide 100 4
# Output: 25.0
```

---

## What Just Happened?

Let's break down what SOMAS did for you:

1. **Requirements Analysis** (Planner)
   - Extracted 4 main features
   - Identified error handling requirements
   - Defined CLI interface needs

2. **System Design** (Architect)
   - Designed 3 main components
   - Specified interfaces
   - Chose appropriate libraries

3. **Implementation** (Implementer)
   - Generated ~200-300 lines of production code
   - Implemented error handling
   - Added input validation

4. **Testing** (Tester)
   - Created ~20-30 test cases
   - Achieved 85%+ coverage
   - Tested edge cases (division by zero, invalid inputs)

5. **Quality Assurance** (Reviewer + Security)
   - Verified code quality
   - Checked for vulnerabilities
   - Validated best practices

6. **Documentation** (Documenter)
   - Created comprehensive README
   - Added usage examples
   - Wrote installation instructions

**Total Time**: 30-60 minutes (autonomous, varies by project complexity)  
**Your Time**: 10-15 minutes (review and approval)

---

## Next Steps

Now that you've created your first SOMAS project, try:

### More Complex Projects

#### API Service
```
Project: REST API for a Todo application
Features:
- Create, read, update, delete todos
- User authentication
- SQLite database
- API documentation
```

#### Data Processing Script
```
Project: CSV data analyzer
Features:
- Read CSV files
- Calculate statistics (mean, median, mode)
- Generate summary reports
- Export to JSON/HTML
```

#### Web Scraper
```
Project: News article scraper
Features:
- Scrape articles from RSS feeds
- Extract title, content, and metadata
- Store in database
- Export to various formats
```

---

## Customization Tips

### Providing Better Requirements

The more specific your requirements, the better the results:

✅ **Good**:
```
Create a CLI calculator that:
- Supports +, -, *, / operations
- Accepts two numbers as arguments
- Returns result to stdout
- Exits with code 1 on errors
- Provides --help flag
- Uses Python 3.10+
```

❌ **Too Vague**:
```
Make a calculator
```

### Specifying Constraints

Help guide the implementation:
```
Technical Constraints:
- Must use argparse (not click)
- No external dependencies except standard library
- Follow Google Python Style Guide
- Include type hints
- Support Python 3.8+
```

### Defining Edge Cases

Mention important edge cases:
```
Edge cases to handle:
- Division by zero → error message
- Invalid numbers → clear error
- Too many/few arguments → show usage
- --help flag → show documentation
```

---

## Troubleshooting Your First Project

### Issue: Pipeline Didn't Start

**Symptoms**: No branch or PR created after adding label

**Solutions**:
1. Verify the label is exactly `somas-project` (case-sensitive)
2. Check if GitHub Actions is enabled in the repository
3. Wait a few minutes (sometimes there's a delay)
4. Check the Actions tab for workflow errors

### Issue: Stage Appears Stuck

**Symptoms**: Stage running for a very long time

**Solutions**:
1. Check the Actions logs for errors
2. Verify agent configurations are valid
3. Check if iteration limit was reached
4. Wait patiently (complex stages can take time)

### Issue: Tests Failing

**Symptoms**: Validation stage reports test failures

**Solutions**:
1. Review test output in the workflow logs
2. Check if dependencies are missing
3. Look for environment-specific issues
4. Add comments on PR requesting fixes
5. The pipeline should automatically retry

### Issue: Code Doesn't Meet Expectations

**Symptoms**: Generated code doesn't work as expected

**Solutions**:
1. Review the requirements in your original issue
2. Add detailed comments on the PR explaining issues
3. Close the PR and create a new issue with clearer requirements
4. Manually refine the generated code

---

## Tips for Success

1. **Be Specific**: Detailed requirements lead to better results
2. **Specify Technology**: Mention preferred languages/frameworks
3. **Define Constraints**: List any technical requirements
4. **Mention Edge Cases**: Call out important scenarios
5. **Review Thoroughly**: Always review generated code
6. **Iterate if Needed**: Don't hesitate to request changes
7. **Learn from Output**: Study the generated code to learn patterns

---

## Learning Resources

- **[Full Documentation](README.md)**: Complete SOMAS guide
- **[Agent Configurations](../../.somas/agents/)**: How agents work
- **[Templates](../../.somas/templates/)**: Planning and architecture templates
- **[Design Patterns](../../.somas/patterns/)**: Common patterns used

---

## Getting Help

If you encounter issues:

1. **Check Documentation**: Review this guide and the main docs
2. **Search Issues**: Look for similar problems
3. **Create an Issue**: Open a new issue (not a SOMAS project request)
4. **Contact Owner**: Mention @scotlaclair for assistance

---

## Ready for More?

Now that you've completed your first project, you're ready to:
- Build more complex applications
- Experiment with different project types
- Customize agent configurations
- Integrate with your workflows

**Happy building with SOMAS!** 🚀
