package com.makestoryai.data.api

import com.makestoryai.data.model.GeneratedStory
import com.makestoryai.data.model.StoryRequest
import retrofit2.http.Body
import retrofit2.http.POST

interface StoryApi {
    @POST("api/v1/generate")
    suspend fun generateStory(@Body request: StoryRequest): GeneratedStory
}
