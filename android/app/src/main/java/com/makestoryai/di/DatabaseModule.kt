package com.makestoryai.di

import android.content.Context
import androidx.room.Room
import com.makestoryai.data.database.AppDatabase
import com.makestoryai.data.database.StoryDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "make_story_db"
        ).build()
    }

    @Provides
    @Singleton
    fun provideStoryDao(database: AppDatabase): StoryDao {
        return database.storyDao()
    }
}
