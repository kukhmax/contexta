package com.makestoryai.data.model

import com.google.gson.annotations.SerializedName

data class StoryRequest(
    @SerializedName("topic") val topic: String,
    @SerializedName("level") val level: String,
    @SerializedName("language") val language: String
)

data class GeneratedStory(
    @SerializedName("title") val title: String,
    @SerializedName("story_html") val storyHtml: String,
    @SerializedName("forms") val forms: List<WordForm>,
    @SerializedName("audio_url") val audioUrl: String?
)

data class WordForm(
    @SerializedName("form") val form: String,
    @SerializedName("base") val base: String,
    @SerializedName("tense") val tense: String,
    @SerializedName("translation") val translation: String
)
