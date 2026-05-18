from pydantic import BaseModel, ConfigDict, Field


class ProductSpecItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        description="The specification name, such as display, processor, RAM, storage, or battery."
    )
    value: str = Field(
        description="The specification value exactly as stated or clearly implied by the transcript."
    )


class ProductSpecification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(
        description="The product name or model mentioned in the video."
    )
    brand: str | None = Field(
        default=None,
        description="The product brand or manufacturer, if mentioned.",
    )
    category: str | None = Field(
        default=None,
        description="The product category, such as smartphone, laptop, GPU, or headphones.",
    )
    specifications: list[ProductSpecItem] = Field(
        default_factory=list,
        description="Technical specifications explicitly mentioned in the video.",
    )
    notable_features: list[str] = Field(
        default_factory=list,
        description="Important review notes, features, strengths, or weaknesses mentioned.",
    )
    price: str | None = Field(
        default=None,
        description="Price or price range mentioned in the video.",
    )
    availability: str | None = Field(
        default=None,
        description="Availability, launch, region, or purchase information mentioned.",
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Short transcript-based evidence snippets used for extraction.",
    )


class ProductSpecsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    video_id: str
    products: list[ProductSpecification]
