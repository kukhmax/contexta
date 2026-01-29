package com.makestoryai.data.database

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.WordForm
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

@Entity(tableName = "stories")
data class StoryEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val storyHtml: String,
    val formsJson: String, // Store list as JSON string for simplicity
    val audioUrl: String?,
    val timestamp: Long = System.currentTimeMillis()
) {
    fun toDomain(): GeneratedStory {
        val type = object : TypeToken<List<WordForm>>() {}.type
        val forms = Gson().fromJson<List<WordForm>>(formsJson, type) ?: emptyList()
        return GeneratedStory(title, storyHtml, forms, audioUrl)
    }

    companion object {
        fun fromDomain(story: GeneratedStory): StoryEntity {
            val formsJson = Gson().toJson(story.forms)
            return StoryEntity(
                title = story.title,
                storyHtml = story.storyHtml,
                formsJson = formsJson,
                audioUrl = story.audioUrl
            )
        }
    }
}
