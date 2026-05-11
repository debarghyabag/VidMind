from langchain_core.prompts import ChatPromptTemplate
from app.models.schemas.summary_schema import SummaryResponse
from app.utils.llm_client import llm

def summarize_video(video_id: str, chunks: list[dict]) -> SummaryResponse:
    video_content = "\n".join(
        f"[{chunk['start_time']:.2f}-{chunk['end_time']:.2f}] {chunk['text']}"
        for chunk in chunks
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You summarize YouTube transcript chunks. Return only the requested structured output.",
            ),
            (
                "human",
                "Video ID: {video_id}\n\nTranscript chunks:\n{video_content}",
            ),
        ]
    )

    structured_llm = llm.with_structured_output(SummaryResponse)
    chain = prompt | structured_llm

    return chain.invoke(
        {
            "video_id": video_id,
            "video_content": video_content,
        }
    )
