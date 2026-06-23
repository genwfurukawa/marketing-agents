# Claude Code Mastery Guide

**How to discover and use EVERYTHING at your disposal**

---

## 🎯 Your Available Capabilities

You have access to 4 categories of capabilities:

1. **Tools** - Direct actions Claude Code can perform
2. **MCP Servers** - External integrations and data sources  
3. **Slash Commands** - Custom workflows you've defined
4. **Agents** - Specialized AI assistants for complex tasks

---

## 1️⃣ DISCOVERING YOUR TOOLS

### What Are Tools?

Tools are Claude Code's built-in capabilities for interacting with your system.

### How to See All Available Tools

**Method 1: Ask Claude**
```
"What tools do you have access to?"
"List all tools available in this workspace"
```

**Method 2: Check Documentation**
- Claude Code has standard tools that are always available
- Custom tools may be added via MCP servers

### Standard Claude Code Tools

Based on your current setup, you have:

#### File Operations
- **Read** - Read any file
- **Write** - Create new files
- **Edit** - Modify existing files
- **Glob** - Find files by pattern
- **Grep** - Search file contents

#### Execution
- **Bash** - Run shell commands
- **NotebookEdit** - Edit Jupyter notebooks

#### Web & Research
- **WebFetch** - Fetch and analyze web pages
- **WebSearch** - Search the web
- **ReadMcpResourceTool** - Read MCP resources
- **ListMcpResourcesTool** - List MCP resources

#### Workflow & Planning
- **Task** - Launch specialized agents
- **TaskOutput** - Get results from background tasks
- **EnterPlanMode** - Plan complex implementations
- **ExitPlanMode** - Finalize and execute plans
- **TodoWrite** - Track progress with todos
- **AskUserQuestion** - Get user input during execution
- **SlashCommand** - Execute custom commands
- **Skill** - Run predefined skills

#### Your Custom MCP Tools
- **mcp__actors-mcp-server__search-apify-docs**
- **mcp__actors-mcp-server__fetch-apify-docs**  
- **mcp__actors-mcp-server__apimaestro-slash-linkedin-profile-posts** ← LinkedIn scraper!
- **mcp__actors-mcp-server__get-actor-output**

---

## 2️⃣ DISCOVERING YOUR MCP SERVERS

### What Are MCP Servers?

MCP (Model Context Protocol) servers are external integrations that give Claude Code special powers.

### Your Current MCP Server

**actors-mcp-server** (Apify integration)
- **Purpose:** Web scraping and data extraction
- **Main capability:** LinkedIn profile scraping

### How to Use MCP Tools

**Example: LinkedIn Research**
```
"Use the LinkedIn profile scraper to analyze competitor posts from username 'competitor-username'"
```

Claude will automatically use: `mcp__actors-mcp-server__apimaestro-slash-linkedin-profile-posts`

### Finding MCP Resources

```
"List all MCP resources available"
"What can the actors-mcp-server do?"
```

### Adding More MCP Servers (Future)

You can add servers for:
- Google Drive integration
- Notion integration
- Database access
- API integrations
- Custom data sources

**How:** Update `.claude/settings.json` or global Claude Code settings

---

## 3️⃣ DISCOVERING YOUR SLASH COMMANDS

### What Are Slash Commands?

Custom workflows you've defined. They're like macros or shortcuts.

### Your Current Slash Commands

**Global Command:**
- `/init_client` - Initialize new client workspace

**Client-Specific Commands** (when in client workspace):
- `/linkedin_strategy` - Create content strategy
- `/linkedin_calendar` - Generate monthly calendar
- `/linkedin_post` - Create single post
- `/linkedin_batch` - Batch generate posts
- `/linkedin_review` - Review post quality
- `/linkedin_research` - Analyze competitors (MCP)
- `/linkedin_analytics` - Performance reports
- `/upgrade_client` - Add enhanced features to existing client

### How to See Available Commands

**Method 1: Ask**
```
"What slash commands are available?"
"List all /linkedin commands"
```

**Method 2: Check Files**
```bash
# Global commands
ls .claude/commands/

# Client commands  
ls {client_root}/00_admin/commands/
```

### How to Create Your Own Slash Command

**Step 1: Create file in `.claude/commands/` or `00_admin/commands/`**

```markdown
---
description: What this command does
args:
  - name: argument_name
    description: What this argument is
    required: true
---

Instructions for Claude on what to do when this command is run.

Use {{argument_name}} to reference the argument.

Example steps:
1. Read files from [location]
2. Process using [method]
3. Output to [destination]
```

**Step 2: Save as `command_name.md`**

**Step 3: Use it:** `/command_name argument_value`

---

## 4️⃣ DISCOVERING AND USING AGENTS

### What Are Agents?

Specialized AI assistants that can run complex, multi-step tasks autonomously.

### Agent Types Available to You

#### Built-in Claude Code Agents

1. **general-purpose**
   - For complex multi-step tasks
   - Can search code, read files, make decisions
   - Use when task requires multiple steps

2. **Explore**
   - Fast codebase exploration
   - Find files by patterns
   - Answer questions about codebase
   - Thoroughness levels: quick, medium, very thorough

3. **Plan**
   - Software architect agent
   - Design implementation plans
   - Identify critical files
   - Consider trade-offs

4. **claude-code-guide**
   - Expert on Claude Code itself
   - Answers questions about features
   - Helps with configuration
   - SDK and API guidance

#### Your Custom Agents

Located in: `{client_root}/00_admin/agents/`

1. **Hook Optimizer Agent**
   - Analyzes and improves post hooks
   - Scores effectiveness
   - Generates alternatives

2. **Voice Consistency Agent**
   - Checks brand voice alignment
   - Flags off-brand language
   - Suggests corrections

3. **Social Media Coordinator Agent** (NEW!)
   - Meta-agent that orchestrates workflow
   - Calls other agents as needed
   - Manages full content lifecycle

### How to Launch an Agent

**Method 1: Using Task Tool (Recommended)**
```
Task(
  subagent_type="general-purpose",
  description="Short description",
  prompt="Detailed instructions for what the agent should do"
)
```

**Method 2: Natural Language**
```
"I need an agent to analyze competitor LinkedIn content and create a strategy report"
```

Claude will automatically choose the right agent type and spawn it.

**Method 3: Resume Previous Agent**
```
Task(
  subagent_type="general-purpose",
  resume="agent-id-from-previous-run",
  description="Continue previous work",
  prompt="Additional instructions"
)
```

### Agent Examples

#### Example 1: Research Agent
```
"Launch a general-purpose agent to:
1. Read all files in 02_research/competitors/
2. Analyze patterns across competitors
3. Generate strategic recommendations
4. Save report to 02_research/competitive_summary.md"
```

#### Example 2: Hook Optimizer
```
"Use the Hook Optimizer approach to analyze this hook:

'Most AI projects fail in production.
Not because the model isn't good enough.'

Provide:
- Effectiveness score
- 3 alternative hooks
- Recommendation"
```

#### Example 3: Social Media Coordinator
```
"Act as social media coordinator for Iterate.ai:

1. Read this week's calendar
2. Generate 4 posts using /linkedin_batch
3. Optimize each hook
4. Check voice consistency
5. Provide ready-to-publish report"
```

#### Example 4: Parallel Agents
```
"Launch 3 agents in parallel:

Agent 1: Research competitor A's LinkedIn
Agent 2: Research competitor B's LinkedIn  
Agent 3: Analyze our current content strategy

Compile findings into unified report"
```

### Creating Agents That Create Agents

**The Meta-Agent Pattern:**

```markdown
# Workflow Orchestrator Agent

You are a workflow orchestrator. Your job is to:

1. Analyze the task
2. Break it into subtasks
3. Spawn specialized agents for each subtask
4. Coordinate their outputs
5. Compile unified result

Example workflow:
- Spawn Research Agent → Get competitor data
- Wait for completion
- Spawn Strategy Agent → Use research to create strategy
- Wait for completion  
- Spawn Content Agent → Create posts based on strategy
- Compile and report
```

**Usage:**
```
"I need a meta-agent to handle the full monthly LinkedIn workflow"
```

The meta-agent will spawn:
- Research sub-agents
- Strategy sub-agents
- Content creation sub-agents
- Quality check sub-agents
- Analytics sub-agents

---

## 🔍 HOW TO DISCOVER WHAT YOU HAVE

### Quick Discovery Commands

```bash
# See all slash commands
ls -la .claude/commands/
# Client commands are in external workspaces: ../clients/*/00_admin/commands/

# See all agents
# Client agents are in external workspaces: ../clients/*/00_admin/agents/

# See all workflows
# Client workflows are in external workspaces: ../clients/*/00_admin/workflows/

# See MCP configuration
cat .claude/settings.local.json

# See all templates
ls -la 00_templates/linkedin_system/
```

### Ask Claude Directly

```
"Show me everything I can do with LinkedIn content in this workspace"
"What MCP servers do I have access to?"
"List all available agents"
"What tools can you use?"
"Show me the full workflow for creating LinkedIn content"
```

---

## 💡 POWER USER PATTERNS

### Pattern 1: Agent Swarms

Launch multiple agents to work in parallel:

```
"I need a swarm of agents:

1. Research Agent → Analyze 3 competitors
2. Strategy Agent → Update pillars based on research
3. Content Agent → Generate Week 1 posts
4. Quality Agent → Review and score all posts
5. Coordinator Agent → Compile everything

Run in parallel where possible, coordinate results"
```

### Pattern 2: Recursive Agents

Agent that creates agents:

```
"Create a supervisor agent that:
1. Reads the monthly calendar
2. For each week, spawns a Content Generation Agent
3. For each post, spawns a Hook Optimizer Agent
4. Compiles all results into monthly package
5. Reports status and quality scores"
```

### Pattern 3: Feedback Loops

Agent that improves itself:

```
"Create a self-improving content agent:

1. Generate post
2. Spawn Hook Optimizer → Get score
3. If score < 8, regenerate with feedback
4. Repeat until score >= 8
5. Spawn Voice Checker → Verify consistency
6. If < 90%, adjust and re-check
7. Return when both thresholds met"
```

### Pattern 4: Conditional Workflows

Agent that adapts based on context:

```
"Smart workflow agent:

IF strategy doesn't exist:
  → Spawn Strategy Creation Agent
ELSE:
  → Read existing strategy

IF this month's calendar missing:
  → Spawn Calendar Generator Agent
ELSE:
  → Read existing calendar

THEN:
  → Spawn Content Creation Agent with context
  → Spawn Quality Review Agent
  → Report results"
```

---

## 📚 LEARNING RESOURCES

### Built-in Help

```
"How do I use the Task tool to spawn agents?"
"Explain MCP servers"
"Show me how to create a slash command"
"What's the difference between agents and tools?"
```

### Your Documentation

1. **System Guides:**
   - `SETUP_COMPLETE.md` - What's been created
   - `ENHANCED_FEATURES.md` - Advanced capabilities
   - `HOW_TO_SCALE_ENHANCEMENTS.md` - Replication guide

2. **Client Guides:**
   - `{client_root}/START_HERE.md` - Navigation
   - `{client_root}/GETTING_STARTED.md` - Walkthrough
   - `{client_root}/QUICK_START.md` - Quick reference

3. **Agent Guides:**
   - `{client_root}/00_admin/agents/` - All agent docs

4. **Workflow Guides:**
   - `{client_root}/00_admin/workflows/` - Process docs

### Online Resources

```
"Search Apify documentation for Actor development"
"Fetch Claude Code documentation about MCP servers"
```

---

## 🎯 QUICK REFERENCE

| Need | Use This | Example |
|------|----------|---------|
| **Run custom workflow** | Slash command | `/linkedin_batch week="Week 1"` |
| **Scrape LinkedIn** | MCP tool | "Analyze competitor-username's LinkedIn" |
| **Complex multi-step task** | Agent (Task tool) | "Research competitors and create strategy" |
| **Read/write files** | Built-in tools | "Read the strategy file" |
| **Search code** | Grep/Glob tools | "Find all posts about AI" |
| **Web research** | WebSearch/WebFetch | "Search for LinkedIn best practices 2025" |
| **Parallel work** | Multiple agents | "Launch 3 agents to research competitors" |
| **Plan implementation** | Plan mode | EnterPlanMode → design → ExitPlanMode |
| **Track progress** | TodoWrite | Automatic todo tracking |

---

## 🚀 PUTTING IT ALL TOGETHER

### Ultimate Workflow Example

```
User: "Set up complete LinkedIn system for Iterate.ai for January"

Claude orchestrates:

1. [Tool: Read] → Check if research exists
2. [MCP: LinkedIn Scraper] → Analyze 3 competitors
3. [Agent: Strategy] → Create content pillars from research
4. [Slash Command] → /linkedin_calendar month="January 2025"
5. [Agent Swarm] → 4 Content Agents (one per week)
   └─> Each spawns Hook Optimizer sub-agents
   └─> Each spawns Voice Consistency sub-agents
6. [Agent: Quality Review] → Score all posts
7. [Tool: Write] → Compile monthly package
8. [Report] → Status, quality scores, ready to publish

All coordinated by Social Media Coordinator Agent
Result: 20 posts ready, optimized, on-brand, scheduled
```

---

**You now have a complete AI-powered content production system with:**
- ✅ 10+ built-in tools
- ✅ 4+ MCP integrations
- ✅ 8 custom slash commands
- ✅ 5+ specialized agents
- ✅ Unlimited agent combinations

**Next:** Try it! Start with simple commands, experiment with agents, build your own workflows.
