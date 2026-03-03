# Week 3: Pharmaceutical Information Assistant with LLM Tool Calling

A progressive exploration of building AI-powered applications using OpenAI's function calling API, demonstrated through an evolving pharmaceutical information system.

## 📋 Overview

This week covers the complete journey from basic tool calling to a sophisticated multi-tool pharmaceutical assistant. The project demonstrates how to integrate LLMs with external data sources (APIs, databases) through structured function calls.

### Project Structure

```
week3/
├── exp_01_FlightAI.ipynb              # Foundation: Basic tool calling with flight pricing
├── MedProfile_Phase1_DrugInfo_Lookup.ipynb     # Single tool: FDA drug lookup
├── MedProfile_Phase2_MultiSourceAggregation.ipynb   # Dual tools: Local DB + FDA API
├── MedProfile_Phase3_MultiToolingInteractions.ipynb # Five tools: Comprehensive assistant
├── services/
│   ├── __init__.py
│   ├── openfda_api.py                 # FDA API wrapper
│   ├── medicine_dbutil.py             # Medicine database (11,825 records)
│   ├── interactions_dbutil.py         # Drug interaction database (80 records)
│   ├── comprehensive_drug_dbutil.py   # Comprehensive drug database (718 records)
│   ├── phase2_medicine_llm_schema.py  # Two-tool schema definition
│   └── phase3_medicine_llm_schema.py  # Five-tool schema definition
└── db/                                # SQLite databases (auto-created)
    ├── medicine_info.db
    ├── drug_interactions.db
    └── comprehensive_drug.db
```

---

## 🎯 Learning Path

### **Phase 0: Foundation (exp_01_FlightAI.ipynb)**
**Concept**: Understanding basic tool calling mechanics

- **Single tool call**: Basic request-response
- **Multiple tool calls**: Simultaneous execution in one iteration
- **Sequential tool calls**: Iterative chaining (v3 with `while` loop)
- **Key learning**: How LLMs decide when to call tools and how results flow back

**Tool**: `ticket_price_checker`
- Input: destination city
- Output: ticket price or not found message

---

### **Phase 1: Single Tool Integration (MedProfile_Phase1_DrugInfo_Lookup.ipynb)**
**Concept**: Integrating external APIs with LLM

- Single tool: `drug_lookup` (queries FDA API)
- Handles tool argument parsing from JSON
- Implements error handling for API failures
- Uses max iteration limit to prevent infinite loops
- **Output**: Drug information including warnings and indications

**Dataset**: OpenFDA API (real-time)

---

### **Phase 2: Multi-Source Aggregation (MedProfile_Phase2_MultiSourceAggregation.ipynb)**
**Concept**: Coordinating multiple data sources

Two tools working in sequence:
1. **get_medicine_info**: Local SQLite database (11,825 medicines)
   - Brand names, compositions, manufacturers
   - Uses and side effects
   - Fast local queries

2. **drug_lookup**: OpenFDA API
   - Official FDA warnings
   - Active ingredients
   - Comprehensive safety data

**Strategy**: LLM automatically decides which tool to use based on user query
- Database lookup for local medicine information
- FDA lookup for official safety data
- Often calls both tools in sequence for comprehensive information

**Databases**: 
- medicine_info.db with indexes on medicine_name and composition

---

### **Phase 3: Comprehensive Multi-Tool System (MedProfile_Phase3_MultiToolingInteractions.ipynb)**
**Concept**: Building a production-grade pharmaceutical assistant

Five integrated tools:

1. **get_medicine_info**: Local medicine database search
2. **drug_lookup**: FDA drug label information
3. **check_drug_interactions**: Drug-drug interaction checker
   - Severity levels: Major, Moderate, Minor
   - Clinical management recommendations
   - Safer alternatives

4. **get_therapeutic_alternatives**: Find drugs in the same class
   - Queries comprehensive_drug.db by drug_class
   - Returns comparable medications
   - Includes availability (OTC vs Prescription)

5. **compare_drugs**: Side-by-side comparison
   - Multiple drugs in single query
   - Detailed comparison across all fields
   - Helps users make informed decisions

**Databases**:
- medicine_info.db (11,825 records)
- drug_interactions.db (80 interactions)
- comprehensive_drug.db (718 drugs with detailed classification)

---

## 🛠️ Technical Architecture

### Tool Calling Flow

```
┌─────────────────┐
│  User Message   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ LLM with Tools + System Prompt       │
│ - Analyzes user intent               │
│ - Decides which tools to call        │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Check finish_reason == "tool_calls"  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Parse Tool Call Arguments (JSON)     │
│ - Extract function name              │
│ - Extract parameters                 │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Execute Function Handler             │
│ - Call appropriate service           │
│ - Handle errors gracefully           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Format Results as Tool Response      │
│ - role: "tool"                       │
│ - tool_call_id: match request        │
│ - content: JSON stringified result   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Add to Message History               │
│ - Continue loop if more tools needed │
│ - Otherwise generate final response  │
└─────────────────────────────────────┘
```

### Database Architecture

**Three Specialized Databases**:

| Database | Records | Purpose | Key Fields |
|----------|---------|---------|-----------|
| medicine_info.db | 11,825 | Brand name lookup | medicine_name, composition, uses, side_effects |
| drug_interactions.db | 80 | Interaction checking | drug_a, drug_b, severity, mechanism |
| comprehensive_drug.db | 718 | Drug classification & comparison | generic_name, drug_class, indications, contraindications |

**Indexing Strategy**:
- Medicine name for fast brand lookup
- Composition for generic name search
- Drug class for finding alternatives
- Drug pairs for interaction queries

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install openai gradio pandas requests python-dotenv
```

### Environment Setup
Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

### Running Phase 3 (Recommended)
```python
python MedProfile_Phase3_MultiToolingInteractions.ipynb
```

The application will:
1. Auto-create three SQLite databases
2. Import data from CSV and JSON files
3. Launch Gradio interface at http://127.0.0.1:7876

### Example Queries
```
"Tell me about Aspirin"
→ Uses get_medicine_info + drug_lookup

"What if I take Aspirin and Ibuprofen together?"
→ Uses check_drug_interactions

"Show me other pain relievers like Aspirin"
→ Uses get_therapeutic_alternatives

"Compare Aspirin, Ibuprofen, and Naproxen"
→ Uses compare_drugs
```

---

## 📊 Key Concepts

### System Prompts
Each phase includes a carefully crafted system prompt that:
- Defines the assistant's role and constraints
- Lists available tools and their purposes
- Provides rules for when/how to use tools
- Emphasizes safety and accuracy

**Example (Phase 3)**:
```
You are a comprehensive pharmaceutical information assistant.

You have access to five tools:
1. get_medicine_info: Search local database
2. drug_lookup: Query OpenFDA API
3. check_drug_interactions: Check drug-drug interactions
4. get_therapeutic_alternatives: Find drugs in same class
5. compare_drugs: Compare multiple drugs

When a user asks about medications:
- Use appropriate tool(s) based on their question
- Present information clearly and organized
- Always emphasize warnings and safety information
- Never provide medical advice—only factual information
- Remind users to consult healthcare professionals
```

### Error Handling Patterns

1. **JSON Parsing**:
```python
try:
    args = json.loads(tool_call.function.arguments)
except json.JSONDecodeError as e:
    print(f"Error parsing arguments: {e}")
    args = {}
```

2. **API Failures**:
```python
if response.status_code == 200:
    # Process results
else:
    return {"error": f"API failed with status: {response.status_code}"}
```

3. **Database Errors**:
```python
try:
    cursor.execute(query)
except sqlite3.Error as e:
    print(f"Database error: {e}")
    return None
```

4. **Iteration Limits**:
```python
max_iterations = 5
iteration = 0
while response.choices[0].message.tool_calls and iteration < max_iterations:
    iteration += 1
    # Process tools...
```

### Handling Gradio's History Format
```python
def chat_function(message, history):
    # history items may have content as list
    for h in history:
        content = h["content"]
        if isinstance(content, list):
            content = content[0]["text"] if content else ""
        messages.append({
            "role": h["role"],
            "content": content
        })
```

---

## 📈 Progression & Complexity

### Evolution of Capabilities

| Phase | Tools | Features | Complexity |
|-------|-------|----------|-----------|
| FlightAI | 1 | Basic tool calling, sequential calls | Beginner |
| Phase 1 | 1 | API integration, error handling | Intermediate |
| Phase 2 | 2 | Multi-source coordination, dual queries | Intermediate |
| Phase 3 | 5 | Full pharmaceutical ecosystem, domain logic | Advanced |

### Complexity Increase Points
1. **Single to multiple tools**: Need intelligent dispatch logic
2. **API integration**: Handle timeouts, errors, rate limiting
3. **Multiple databases**: Coordinate results from different sources
4. **Domain-specific logic**: Tool handlers contain business rules (e.g., finding alternatives by drug class)

---

## 🔍 Important Implementation Details

### Tool Schema Definition
```python
tool = {
    "type": "function",
    "function": {
        "name": "drug_lookup",
        "description": "Query OpenFDA API for drug label information...",
        "parameters": {
            "type": "object",
            "properties": {
                "generic_name": {
                    "type": "string",
                    "description": "The generic name of the drug..."
                }
            },
            "required": ["generic_name"]
        }
    }
}
```

### Tool Call Handling Pattern
```python
def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        # Parse arguments
        args = json.loads(tool_call.function.arguments)
        
        # Execute appropriate function
        if tool_call.function.name == "drug_lookup":
            result = drug_lookup(args.get("generic_name"))
        
        # Format response
        response = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
        responses.append(response)
    
    return responses
```

### Iteration Loop
```python
while response.choices[0].finish_reason == "tool_calls":
    # Add assistant message with tool calls
    messages.append({
        "role": "assistant",
        "content": response.choices[0].message.content,
        "tool_calls": response.choices[0].message.tool_calls
    })
    
    # Execute tools and add results
    tool_responses = handle_tool_calls(response.choices[0].message)
    messages.extend(tool_responses)
    
    # Get next response
    response = client.chat.completions.create(
        model=curr_model,
        messages=messages,
        tools=tools
    )

# Return final response
return response.choices[0].message.content
```

---

## 📚 Key Features by Phase

### exp_01_FlightAI.ipynb
✅ Basic tool calling  
✅ Multiple simultaneous tool calls  
✅ Sequential/iterative tool calls (v3)  
✅ Gradio chat interface  

### MedProfile_Phase1_DrugInfo_Lookup.ipynb
✅ API integration (OpenFDA)  
✅ JSON argument parsing  
✅ Error handling  
✅ Max iteration limits  

### MedProfile_Phase2_MultiSourceAggregation.ipynb
✅ Dual data sources (DB + API)  
✅ Database with 11,825 medicines  
✅ Intelligent tool dispatch  
✅ Multi-phase queries  

### MedProfile_Phase3_MultiToolingInteractions.ipynb
✅ Five integrated tools  
✅ Drug interaction checking  
✅ Therapeutic alternatives  
✅ Drug comparison  
✅ 718-drug comprehensive database  
✅ Domain-specific business logic  

---

## 🧪 Testing & Validation

### Built-in Tests
Each notebook includes validation:
```python
# Test direct function calls before chat
aspirin_info = get_medicine_info("Aspirin")
for result in aspirin_info:
    print(result)

# Verify database imports
cursor.execute('SELECT COUNT(*) FROM medicines')
count = cursor.fetchone()[0]
print(f"Total medicines: {count}")

# Test interactions
interaction = check_drug_interaction("Aspirin", "Warfarin")
print(interaction)
```

### Sample Outputs Included
- Direct function test results
- API response samples
- Database query results
- Chat interface outputs with complete message flows

---

## ⚙️ Configuration

### Model Selection
```python
# OpenAI hosted (recommended)
gpt_model = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
curr_model = gpt_model

# Or local Ollama models (commented out)
# mistral_model = "mistral:latest"
# llama_model = "llama3.2:1b"
```

### Temperature Settings
- All implementations use `temperature=0`
- Reason: Deterministic responses appropriate for tool calling and factual queries

### Iteration Limits
- Default: `max_iterations = 5`
- Purpose: Prevent infinite loops with circular tool calls

---

## 🔐 Safety & Best Practices

### System Prompt Constraints
- Clear boundaries on assistant capabilities
- No medical advice (only factual information)
- Emphasis on consulting healthcare professionals
- Safety warning prioritization

### Data Safety
- Local databases for HIPAA-relevant information
- Validated OpenFDA API for official information
- Error messages don't expose sensitive details
- Input validation for all tool parameters

### Error Messages
- User-friendly without technical jargon
- Actionable suggestions (try alternative search terms)
- Graceful degradation when data unavailable

---

## 📖 Code Examples

### Using Phase 3 API Directly
```python
from services import (
    get_medicine_info,
    drug_lookup,
    check_drug_interaction,
    get_drugs_by_class,
    get_drug_details
)

# Search for a medicine
results = get_medicine_info("Aspirin")

# Get FDA information
fda_data = drug_lookup("Aspirin")

# Check interactions
interaction = check_drug_interaction("Warfarin", "Aspirin")

# Find alternatives in same class
alternatives = get_drugs_by_class("NSAID")

# Get detailed drug info
details = get_drug_details("Ibuprofen")
```

### Building Your Own Tool Handler
```python
def handle_custom_tool(tool_call):
    args = json.loads(tool_call.function.arguments)
    
    if tool_call.function.name == "my_tool":
        result = my_custom_function(args.get("param"))
    
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result)
    }
```

---

## 🎓 Learning Outcomes

After completing this week, you'll understand:

1. **OpenAI Function Calling API**: How to define, call, and handle tool responses
2. **Iterative Tool Calling**: Building sequences where tool results inform subsequent calls
3. **Multi-Source Data Integration**: Coordinating multiple APIs and databases
4. **LLM-Driven Application Logic**: Using LLM to determine which tools to call
5. **Error Handling at Scale**: Managing failures across multiple integrated systems
6. **Domain-Specific AI**: Implementing business logic in tool handlers
7. **Production Patterns**: Iteration limits, result caching, graceful degradation

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError for services
**Solution**: Ensure you're running from the week3 directory
```bash
cd week3
python MedProfile_Phase3_MultiToolingInteractions.ipynb
```

### Issue: "No results found for generic name"
**Cause**: OpenFDA API naming differs from brand names  
**Solution**: Try different generic names (e.g., "acetylsalicylic acid" for Aspirin)

### Issue: Database "already exists" error
**Cause**: Dropping and recreating database mid-session  
**Solution**: Delete db/ folder and restart, or check file permissions

### Issue: Gradio port already in use
**Cause**: Previous process still running  
**Solution**: Find and kill process on port 7876, or modify launch port
```python
gr.ChatInterface(fn=med_tool_chat).launch(server_name="127.0.0.1", server_port=7877)
```

---

## 📝 Notes

- All code uses `temperature=0` for deterministic, factual responses
- Gradio history format may have list-based content—handled with type checking
- OpenFDA API queries are case-sensitive
- Database creation is automatic; datasets must be in correct paths
- Tool execution is sequential within each iteration but can call multiple tools per iteration

---

## 🔗 Resources

- [OpenAI Function Calling Docs](https://platform.openai.com/docs/guides/function-calling)
- [OpenFDA API](https://open.fda.gov/apis/)
- [Gradio Documentation](https://www.gradio.app/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 📄 License

This project is for educational purposes.

---

## 👥 Authors

Week 3 - LLM Tool Calling & Integration  
Educational Project