# Multi-Model Conversational AI with Gradio

A comprehensive exploration of building interactive web-based interfaces for multi-model conversations using local language models served via Ollama and Gradio.

---

## 📋 Overview

This project demonstrates a progressive learning journey from basic model API calls to sophisticated multi-model conversational systems. Through three carefully structured Jupyter notebooks, you'll explore streaming responses, real-time interfaces, and advanced personality-driven model interactions.

**Key Features:**
- Local language model integration via Ollama
- Real-time streaming responses
- Multi-model conversations with distinct personalities
- Interactive web interfaces with Gradio
- Configurable tone-based response generation

---

## 🗂️ Project Structure

### File Organization

**Production/Polished Versions (Recommended):**
- `01_Talking_models.ipynb` - Polished version with improved formatting and organization
- `02_Simple_Gradio_App.ipynb` - Polished version with best practices
- `03_Gradio_Talking_Models.ipynb` - Polished version with advanced patterns

**Experimental/Original Versions:**
- `exp_01_talking_models.ipynb` - Original experimental foundations
- `exp_02_my_simple_gradio_app.ipynb` - Original experimental Gradio implementation
- `exp_03_gradio_talking_models.ipynb` - Original experimental advanced features

> **Recommendation**: Start with the numbered versions (01_, 02_, 03_) for better formatting, clearer headings, and improved code organization. Use experimental versions for reference or direct comparison with original code structure.

---

### 1. **01_Talking_models.ipynb** (Polished) / **exp_01_talking_models.ipynb** (Experimental)
**Foundations: Two-Model Conversations with Contrasting Personalities**

#### What Was Explored:
- Basic API calls to local language models
- System prompts for personality definition
- Single-turn and multi-turn conversations
- Message history management
- Streaming API responses

#### How It Was Achieved:
1. **Setup & Client Initialization**
   - Connected to local Ollama server via OpenAI Python client
   - Configured two models: Mistral and Llama 3.2

2. **Personality Definition**
   - Mistral: Argumentative, challenging chatbot (snarky tone)
   - Llama: Polite, agreeable chatbot (courteous tone)

3. **Non-Streaming Implementation**
   - `call_llama()` and `call_mistral()` functions
   - Maintained message history as lists
   - Demonstrated personality clash in conversation

4. **Streaming Implementation**
   - `call_llama_stream()` and `call_mistral_stream()` generator functions
   - Real-time token-by-token output
   - Word-by-word streaming display in notebook

#### Key Code Patterns:
```python
# Basic API call with system prompt
messages = [
    {'role': 'system', 'content': personality_prompt},
    {'role': 'user', 'content': user_message}
]
response = openai.chat.completions.create(model=model_name, messages=messages)

# Streaming implementation
stream = openai.chat.completions.create(
    model=model_name, 
    messages=messages, 
    stream=True
)
for chunk in stream:
    yield chunk.choices[0].delta.content
```

---

### 2. **02_Simple_Gradio_App.ipynb** (Polished) / **exp_02_my_simple_gradio_app.ipynb** (Experimental)
**Building User-Friendly Chat Interfaces with Gradio**

#### What Was Explored:
- Gradio interface creation for web-based chat
- Text input/output handling
- Markdown rendering of responses
- Real-time streaming in web interfaces
- Example prompts and UI customization

#### How It Was Achieved:
1. **Basic Setup**
   - Imported Gradio framework
   - Established OpenAI client connection
   - Configured Llama model with helpful assistant persona

2. **Non-Streaming Interface (Section 4)**
   - `call_llama()` function for single API calls
   - `gr.Textbox` for input and output
   - `gr.Interface` wrapper for web deployment
   - Pre-loaded example prompts for quick testing

3. **Streaming Web Interface (Section 5)**
   - `stream_llama()` generator for token streaming
   - `gradio_llama_stream()` wrapper that accumulates tokens
   - `gr.Markdown` output for formatted display
   - Real-time progressive updates in browser

4. **Interface Configuration**
   - Input labels with descriptions
   - Multi-line textboxes (7-8 lines)
   - Example prompts covering philosophical themes
   - Disabled flagging for cleaner UX

#### Key Code Patterns:
```python
# Basic Gradio interface
input_textbox = gr.Textbox(label='Your Message', info='Enter a message', lines=7)
output_textbox = gr.Markdown(label='Model response')

view = gr.Interface(
    fn=response_function,
    title='My Chat App',
    inputs=input_textbox,
    outputs=output_textbox,
    examples=[...],
    flagging_mode='never'
)
view.launch()

# Streaming wrapper for Gradio
def gradio_llama_stream(prompt):
    result = ""
    for token in stream_llama(prompt):
        result += token
        yield result  # Progressive updates
```

---

### 3. **03_Gradio_Talking_Models.ipynb** (Polished) / **exp_03_gradio_talking_models.ipynb** (Experimental)
**Advanced: Multi-Model Conversations with Dynamic Personalities**

#### What Was Explored:
- Four distinct personality/tone systems
- Single-model responses with tone selection
- Two-model exchanges with context awareness
- Multi-turn conversations (non-streaming)
- Full streaming multi-turn conversations
- Advanced UI with dropdown selectors and sliders

#### How It Was Achieved:
1. **Tone System Design (Section 1)**
   - **Rational**: Structured logic, analytical clarity
   - **Philosopher**: Reflective, conceptual thinking
   - **Cynic**: Dry cynicism, sharp realism
   - **Adversary**: Strong opposition, counterarguments
   
   Each tone includes specific instructions to keep responses 2-3 sentences (conversation-focused).

2. **Single Model Interface (Section 2)**
   - `model_response()` function with dynamic tone mapping
   - Model selector dropdown: LLama3.2, Mistral, TinyLlama, Phi
   - Tone selector dropdown: Rational, Philosopher, Cynic, Adversary
   - Real-time streaming output
   - Pre-configured example combinations

3. **Two-Model Exchange (Section 3)**
   - `talking_models()` function for single back-and-forth
   - Model 1 responds to prompt
   - Model 2 responds to Model 1's response
   - Both model and tone selection per model
   - Streaming for both exchanges

4. **Multi-Turn Non-Streaming (Section 4)**
   - `call_model()` helper for basic API calls
   - `talking_models()` orchestration function with counter
   - Conversation context accumulation across exchanges
   - Dictionary-based model/tone mapping (cleaner code)
   - Slider control (1-5 exchanges) with default of 3

5. **Advanced Multi-Turn Streaming (Section 5)**
   - `call_model_stream()` for token-by-token output
   - `streaming_models()` orchestrator with full streaming
   - Real-time display of each token as it's generated
   - Label prefixes for speaker identification
   - Progressive conversation building with context

#### Key Code Patterns:
```python
# Tone and model mapping (cleaner approach)
model_map = {
    'LLama3.2': llama_model,
    'Mistral': mistral_model,
    'TinyLlama': tinyllama_model,
    'Phi': phi_model
}

tone_map = {
    'Rational': rational_tone,
    'Philosopher': philosopher_tone,
    'Cynic': cynic_tone,
    'Adversary': adversary_tone
}

sys_model = model_map[selected_model]
sys_tone = tone_map[selected_tone]

# Multi-turn conversation with context
output = ""
conversation = initial_prompt

for i in range(num_exchanges):
    # Model 1 response
    output += f"**{model1} ({tone1}):** "
    yield output
    
    model1_response = ""
    for chunk in call_model_stream(conversation, sys_model1, sys_tone1):
        model1_response += chunk
        output += chunk
        yield output  # Progressive UI updates
    
    conversation += "\n\n" + model1_response
    # ... same for Model 2
```

---

## 🚀 Getting Started

### Prerequisites
```bash
# Required installations
pip install openai
pip install gradio
pip install ipython

# Ollama setup (for local models)
# Download from: https://ollama.ai
# Pull models:
ollama pull llama3.2:1b
ollama pull mistral
ollama pull phi
ollama pull tinyllama
```

### Running the Notebooks

1. **Start Ollama Server**
   ```bash
   ollama serve
   ```
   (Runs on `http://localhost:11434`)

2. **Launch Jupyter**
   ```bash
   jupyter notebook
   ```

3. **Run Notebooks in Recommended Order**
   
   **For Best Formatting & Organization (Recommended):**
   - Start with `01_Talking_models.ipynb` for foundations
   - Progress to `02_Simple_Gradio_App.ipynb` for UI basics
   - Explore `03_Gradio_Talking_Models.ipynb` for advanced features

   **For Original Exploration (Reference):**
   - `exp_01_talking_models.ipynb` - Original experimental version
   - `exp_02_my_simple_gradio_app.ipynb` - Original experimental version
   - `exp_03_gradio_talking_models.ipynb` - Original experimental version

---

## 📚 Learning Progression

### Complexity Curve
```
01_Talking_models: Basic API calls → Message history → Streaming
                          ↓
02_Simple_Gradio_App: Gradio basics → Non-streaming UI → Streaming UI
                          ↓
03_Gradio_Talking_Models: Single model UI → Two models → Multi-turn → Full streaming
```

### Key Concepts by Notebook

| Concept | 01_Talking_models | 02_Simple_Gradio_App | 03_Gradio_Talking_Models |
|---------|-------------------|----------------------|--------------------------|
| API Calls | ✓ | ✓ | ✓ |
| Streaming | ✓ | ✓ | ✓ |
| Gradio UI | | ✓ | ✓ |
| Multi-model | ✓ | | ✓ |
| Personalities | | | ✓ |
| Multi-turn | ✓ | | ✓ |
| Real-time Updates | | ✓ | ✓ |

---

## 💡 Technical Highlights

### 1. **Streaming Implementation**
Real-time token-by-token responses using generator functions:
```python
def stream_response(prompt):
    stream = openai.chat.completions.create(
        model=model_name,
        messages=[...],
        stream=True
    )
    for chunk in stream:
        if content := chunk.choices[0].delta.content:
            yield content
```

### 2. **Gradio Integration**
Progressive accumulation for streaming display:
```python
def gradio_stream_wrapper(prompt):
    accumulated = ""
    for token in stream_response(prompt):
        accumulated += token
        yield accumulated  # Updates UI with full response so far
```

### 3. **Multi-Turn Context Management**
Building conversation history:
```python
conversation = initial_prompt
for exchange in range(num_exchanges):
    response = call_model(conversation, model, tone)
    conversation += "\n\n" + response
    output += format_response(response)
    yield output
```

### 4. **Personality Mapping**
Dynamic tone selection with dictionaries:
```python
tones = {
    'Rational': rational_system_prompt,
    'Philosopher': philosopher_system_prompt,
    # ...
}
selected_tone = tones[user_selection]
```

---

## 🎯 Use Cases

### Educational
- Learn LLM APIs and streaming responses
- Understand system prompts and personality injection
- Practice Gradio interface design

### Research
- Compare different model behaviors
- Test personality consistency across exchanges
- Analyze tone effects on reasoning

### Entertainment
- Generate philosophical debates
- Create personality-based discussions
- Explore model disagreement patterns

### Development
- Template for chatbot applications
- Foundation for multi-agent systems
- UI/UX patterns for LLM interfaces

---

## 🔧 Customization Options

### Add New Models
```python
# In notebook initialization:
new_model = 'new_model_name'
# Update model selectors in Gradio interface
gr.Dropdown(['Model1', 'Model2', 'Model3', 'new_model_name'])
```

### Create Custom Tones
```python
custom_tone = """
Your custom system prompt here.
Define personality, constraints, style.
Keep response to 2-3 sentences.
Stay fully in character.
"""

# Add to tone mapping
tone_map['CustomName'] = custom_tone
```

### Modify Interface Elements
```python
# Customize input/output
input_box = gr.Textbox(
    label='Your Custom Label',
    info='Custom description',
    lines=10,  # Adjust size
    placeholder='Custom hint text'
)
```

### Change Exchange Count
```python
# Slider range in exp_03
counter_slider = gr.Slider(
    1, 10,  # Min, Max (default is 1-5)
    value=5,  # New default
    step=1,
    label='Number of Exchanges'
)
```

---

## 📊 Architecture Comparison

### 01_Talking_models: Direct Model Interaction
```
User Input → System Prompt → Model → Output
                              ↓
                        Message History
```

### 02_Simple_Gradio_App: Single Model with UI
```
Gradio Input → System Prompt → Stream Response → Gradio Output
                    ↓
                  Model
```

### 03_Gradio_Talking_Models: Multi-Model with Personalities
```
Gradio Input → Model1 (Tone1) → Response1 ↓
                                           ├→ Output
              Model2 (Tone2) ← Response1 ↑
                     ↓
              (Iterates for N exchanges)
```

---

## 📈 Performance Notes

### Streaming Advantages
- **User Experience**: Real-time response visible immediately
- **Perceived Speed**: Users see progress, not blank screen
- **Memory**: Tokens processed as they arrive
- **Interactivity**: Can interrupt long responses

### Model Selection Impact
- **Llama 3.2 (1B)**: Fast, good for testing
- **Mistral**: Larger, better reasoning
- **TinyLlama**: Smallest, fastest
- **Phi**: Balanced performance

### Ollama Considerations
- Runs locally (no API costs)
- Requires GPU/sufficient RAM
- First response slower (model loading)
- Subsequent responses faster (cached)

---

## 🐛 Troubleshooting

### Connection Issues
```python
# Verify Ollama running:
curl http://localhost:11434/api/tags

# Check OpenAI client:
response = openai.chat.completions.create(
    model='llama3.2:1b',
    messages=[{'role': 'user', 'content': 'test'}]
)
```

### Model Not Found
```bash
# List available models
ollama list

# Pull missing model
ollama pull model_name
```

### Gradio Port Conflicts
```python
# Specify custom port
view.launch(server_name="127.0.0.1", server_port=7865)
```

### Streaming Stuttering
- Reduce conversation history length
- Use smaller models (Phi, TinyLlama)
- Increase system resources
- Simplify system prompts

---

## 🔮 Future Enhancements

### Potential Additions
- [ ] Multi-language support
- [ ] Conversation history saving/loading
- [ ] Model performance comparison metrics
- [ ] Voice input/output integration
- [ ] Persistent conversation database
- [ ] User preference learning
- [ ] Custom model fine-tuning
- [ ] Debate scoring system

### Advanced Features
- [ ] Async streaming for multiple models
- [ ] WebSocket real-time updates
- [ ] Model ensemble voting
- [ ] Conversation branching (choose best response)
- [ ] Automatic tone recommendation
- [ ] Response quality metrics

---

## 📖 Additional Resources

### Ollama
- **GitHub**: https://github.com/ollama/ollama
- **Docs**: https://ollama.ai/library
- **Models**: Pull from community library

### Gradio
- **Docs**: https://gradio.app/docs
- **Gallery**: https://gradio.app/user_guides
- **Components**: https://gradio.app/guides/components

### OpenAI Python Client
- **Docs**: https://github.com/openai/openai-python
- **Streaming Guide**: Official API documentation
- **Examples**: Community implementations

---

## 🤝 Contributing

### Ways to Extend
1. Add new system prompts for different personalities
2. Create new interface layouts
3. Implement additional models
4. Add conversation analytics
5. Build example use cases

### Share Your Variations
- Document modifications clearly
- Test with multiple models
- Include new examples
- Update this README

---

## 📝 License

This educational project is provided as-is for learning and experimentation.

---

## 🎓 Learning Outcomes

After exploring these three notebooks, you'll understand:

✅ **API Integration**: Calling local language models via OpenAI-compatible interface  
✅ **Streaming**: Implementing real-time token-by-token response generation  
✅ **System Prompts**: Shaping model behavior through instruction engineering  
✅ **Gradio UI**: Building interactive web interfaces without frontend frameworks  
✅ **Multi-Agent Systems**: Coordinating multiple models with different personalities  
✅ **Conversation Management**: Maintaining context across multiple turns  
✅ **UX Patterns**: Creating responsive, intuitive interfaces for LLM applications  

---

## 💬 Getting Help

### If You're Stuck
1. Check the notebook comments and docstrings
2. Review the Architecture Comparison section
3. Test individual components in isolation
4. Check Ollama and Gradio logs for errors
5. Verify all models are properly installed

### Common Questions

**Q: Why use local models instead of OpenAI API?**  
A: Cost-free, privacy-preserving, and perfect for learning and testing.

**Q: Can I use this with GPT models?**  
A: Yes! Just change the base_url and model names in OpenAI client setup.

**Q: How do I make responses faster?**  
A: Use smaller models (Phi, TinyLlama) or reduce conversation history.

**Q: Can multiple users access the same Gradio interface?**  
A: Yes, but they'll share the same Ollama server resources.

---

## 🌟 Key Takeaways

1. **Start Simple, Build Complex**: exp_01 → exp_02 → exp_03
2. **Streaming is Key**: Provides better UX and perceived performance
3. **System Prompts Matter**: Personality engineering shapes responses significantly
4. **Gradio Simplifies UI**: No web dev skills needed for functional interfaces
5. **Context is Crucial**: Multi-turn conversations require careful history management
6. **Local is Powerful**: Ollama + local models = affordable experimentation

---

**Happy Exploring! 🚀**

For questions or insights, refer to the detailed comments within each notebook or explore the official documentation for Ollama and Gradio.