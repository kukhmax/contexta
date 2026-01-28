package com.makestoryai.data.repository

import com.makestoryai.data.api.StoryApi
import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.StoryRequest
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class StoryRepository @Inject constructor(
    private val api: StoryApi
) {
    suspend fun generateStory(topic: String, level: String, language: String): Result<GeneratedStory> {
        return try {
            val response = api.generateStory(StoryRequest(topic, level, language))
            Result.success(response)
        } catch (e: Exception) {
            e.printStackTrace()
            Result.failure(e)
        }
    }
}
