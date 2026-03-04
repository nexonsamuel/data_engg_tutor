# LLM Learner

A hands-on repository exploring advanced LLM techniques and multi-provider AI integration. Each project demonstrates core data engineering concepts through practical, production-grade implementations using local and cloud-based language models.

---

## Week 1: PDF Summarizer & Resume Evaluator

Intelligent document processing system that extracts text from PDFs, intelligently chunks content respecting token limits, and generates summaries using LLMs. Evaluates resumes with hiring-focused insights through multi-stage pipeline processing.

**Techniques**: Token-based chunking, context window management, multi-stage pipeline orchestration, provider abstraction, prompt engineering, configuration management

**Tech Stack**: Python, PyMuPDF, Tiktoken, OpenAI/Anthropic APIs, Ollama (local models), SQLite, Gradio

---

## Week 2: Multi-Model Conversational AI with Gradio

Interactive web-based interface demonstrating real-time streaming responses and personality-driven multi-model conversations. Progressively builds from basic model interactions to sophisticated five-tool systems with dynamic tone selection and multi-turn context awareness.

**Techniques**: API streaming, system prompt engineering for personalities, message history management, real-time progressive UI updates, multi-model orchestration, generator-based streaming

**Tech Stack**: Python, OpenAI SDK, Gradio, Ollama, Markdown rendering, streaming protocols

---

## Week 3: Pharmaceutical Assistant with LLM Tool Calling

Comprehensive multi-tool system demonstrating OpenAI function calling with real-world data integration. Coordinates multiple specialized databases (11K+ medicines, 80 interactions, 718 classified drugs) and external APIs (OpenFDA) to provide intelligent pharmaceutical information retrieval and drug comparison.

**Techniques**: Tool schema definition, JSON argument parsing, iterative tool calling loops, error handling and graceful degradation, multi-source data coordination, interaction severity classification, therapeutic alternative discovery

**Tech Stack**: Python, OpenAI API, SQLite (multi-database), pandas, requests, Gradio, OpenFDA API integration

---

## Future Weeks

More advanced projects exploring vector databases, real-time pipelines, multi-agent systems, and production deployment patterns coming soon.

---

**Get Started**: Refer to individual week READMEs for detailed setup instructions and technical walkthroughs.