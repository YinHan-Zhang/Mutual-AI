import { createRouter, createWebHistory } from 'vue-router'
import Introduction from './views/introduction.vue'
import Number from './views/Number.vue'
import Poetry from './views/poetry.vue'
import TextClassification from './views/TextClassification.vue'
import EmotionSentiment from './views/EmotionSentiment.vue'
import WatermarkRemoval from './views/WatermarkRemoval.vue'

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/introduction',
        },
        {
            path: '/introduction',
            name: 'Introduction',
            component: Introduction,
        },
        {
            path: '/number',
            name: 'Number',
            component:Number,
        },
        {
            path: '/poetry',
            name: 'Poetry',
            component:Poetry,
        },
        {
            path: '/chinese_text_classification',
            name: 'TextClassification',
            component:TextClassification,
        },
        {
            path: '/emotion_sentiment',
            name: 'EmotionSentiment',
            component:EmotionSentiment
        },
        {
            path: '/watermark_removal',
            name: 'WatermarkRemoval',
            component: WatermarkRemoval
        },
    ],
})