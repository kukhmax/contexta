package com.makestoryai.data.repository

import com.makestoryai.data.api.StoryApi
import com.makestoryai.data.database.StoryDao
import com.makestoryai.data.database.StoryEntity
import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.StoryRequest
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class StoryRepository @Inject constructor(
    private val api: StoryApi,
    private val dao: StoryDao
) {
    suspend fun generateStory(topic: String, level: String, language: String): Result<GeneratedStory> {
        return try {
            val response = api.generateStory(StoryRequest(topic, level, language))
            
            // Cache locally
            dao.insertStory(StoryEntity.fromDomain(response))
            
            Result.success(response)
        } catch (e: Exception) {
            e.printStackTrace()
            Result.failure(e)
        }
    }
    
    fun getHistory(): kotlinx.coroutines.flow.Flow<List<GeneratedStory>> {
        return kotlinx.coroutines.flow.map { entities ->
            entities.map { it.toDomain() }
        }
    }
}
