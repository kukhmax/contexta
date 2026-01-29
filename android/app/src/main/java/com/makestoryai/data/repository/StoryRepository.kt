package com.makestoryai.data.repository

import com.makestoryai.data.api.StoryApi
import com.makestoryai.data.database.StoryDao
import com.makestoryai.data.database.StoryEntity
import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.StoryRequest
import com.makestoryai.data.user.UserManager
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class StoryRepository @Inject constructor(
    private val api: StoryApi,
    private val dao: StoryDao,
    private val userManager: UserManager
) {
    suspend fun generateStory(topic: String, level: String, language: String): Result<GeneratedStory> {
        return try {
            val response = api.generateStory(
                userManager.getDeviceId(),
                StoryRequest(topic, level, language)
            )
            
            // Cache locally
            dao.insertStory(StoryEntity.fromDomain(response))
            
            Result.success(response)
        } catch (e: Exception) {
            e.printStackTrace()
            // Handle 402 or other errors
            Result.failure(e)
        }
    }
    
    fun getHistory(): kotlinx.coroutines.flow.Flow<List<GeneratedStory>> {
        return kotlinx.coroutines.flow.map { entities ->
            entities.map { it.toDomain() }
        }
    }
    
    suspend fun getUserStatus(): Result<com.makestoryai.data.model.UserStatus> {
        return try {
            val status = api.getUserStatus(userManager.getDeviceId())
            Result.success(status)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun buyPremium(): Result<com.makestoryai.data.model.UserStatus> {
        return try {
            val status = api.upgradeUser(
                com.makestoryai.data.model.PurchaseRequest(userManager.getDeviceId())
            )
            Result.success(status)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
