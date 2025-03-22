# Gyan Srota

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

### Access answers to all queries related to academics, handbooks, facilities and other aspects of Manipal University Jaipur! 🌻

![Gyan Srota](https://github.com/user-attachments/assets/6fc338fe-b768-4020-bc71-0b55a340f19b)

## About

Gyan Srota is a multi-agent Retrieval Augmented Generation (RAG) framework designed specifically for Manipal University Jaipur students and staff. This advanced system utilizes multiple specialized AI agents to retrieve, process, and generate accurate answers to questions about academics, campus facilities, handbooks, events, and more.

## Routes

The project contains the following routes:

```
/ => Landing page
/login => Login or register page
/chatbot => AI chatbot interface (authorized route)
```

## Getting Started

First, clone the repository:

```bash
git clone https://github.com/yourusername/gyan-srota.git
cd gyan-srota
```

Then, install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

Finally, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

- **Multi-Agent RAG System**: Leverages multiple specialized AI agents working in concert to handle different aspects of information retrieval and response generation
- **University-specific Knowledge Base**: Based on comprehensive Manipal University Jaipur data
- **Real-time Responses**: Get latency free answers to your questions
- **Context-Aware Conversations**: Maintains conversation history for more relevant follow-up responses

## Technology Stack

- **Frontend**: Next.js, React, TailwindCSS
- **Authentication**: NextAuth.js
- **AI Integration**: 
  - Multi-agent orchestration framework
  - Vector database for efficient knowledge retrieval
  - Gemini 1.5 Pro for response generation
  - RAG architecture for grounding responses in factual data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Manipal University Jaipur for providing the knowledge base
