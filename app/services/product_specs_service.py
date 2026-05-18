from langchain_core.prompts import ChatPromptTemplate

from app.models.schemas.product_specs_schema import ProductSpecsResponse
from app.utils.llm_client import llm


def extract_product_specs(video_id: str, chunks: list[dict]) -> ProductSpecsResponse:
    video_content = "\n".join(
        f"[{chunk['start_time']:.2f}-{chunk['end_time']:.2f}] {chunk['text']}"
        for chunk in chunks
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You extract structured tech product specifications from YouTube "
                    "review transcript chunks. The video may review one product or "
                    "compare multiple products. Return every distinct product you can "
                    "identify. Only include specifications, prices, availability, and "
                    "features that are stated in the transcript or directly implied by "
                    "nearby transcript context. Use null or empty collections when a "
                    "field is not available. Return only the requested structured output."
                ),
            ),
            (
                "human",
                "Video ID: {video_id}\n\nTranscript chunks:\n{video_content}",
            ),
        ]
    )

    structured_llm = llm.with_structured_output(ProductSpecsResponse)
    chain = prompt | structured_llm

    return chain.invoke(
        {
            "video_id": video_id,
            "video_content": video_content,
        }
    )
