export async function POST(request: Request) {
    const requestBody = await request.json();
  
    if (!requestBody.inputs) {
      throw new Error("Missing 'inputs' field in the request body");
    }
  
    if (!process.env.HUGGING_FACE_TOKEN) {
      throw new Error("Missing 'Hugging Face Access Token'");
    }
  
    const inputs = requestBody.inputs;
  
    const response = await fetch(
      "https://api-inference.huggingface.co/models/Falconsai/text_summarization",
      {
        headers: {
          Authorization: `Bearer ${process.env.HUGGING_FACE_TOKEN}`,
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({ inputs: inputs }),
      }
    );
  
    if (!response.ok) {
      throw new Error("Request Failed");
    }
  
    const output = await response.json();
  
    return new Response(JSON.stringify(output), {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  