<script lang="ts" setup>
import { deleteLecture, type Lecture } from "@/api/course";
import { defineProps , computed} from "vue";
import { NSpace, NCard, NThing, NAvatar, NIcon, NDescriptions, NDescriptionsItem, NA, NDivider, NButton, NPopconfirm} from "naive-ui";
import { Videocam } from "@vicons/ionicons5";
import {Delete} from "@vicons/carbon"
const prop = defineProps<{
    lecture: Lecture;
    course_id: string;
    lecture_id: string;
    isAdmin: boolean;
    onUpdate: () => void;

}>();

const scheduled_time = computed(() => new Date(prop.lecture.scheduled_time ));

const handleDelete = async () => {
    await deleteLecture(prop.course_id, prop.lecture_id);
    prop.onUpdate();
}

console.log(prop.isAdmin);
</script>

<template>
    <n-card>
        <n-thing>
           <template #avatar>
                <n-avatar> 
                    <n-icon :component="Videocam"> </n-icon>
                </n-avatar>
           </template>
           <template #header>
                {{ prop.lecture.title }}
           </template>
           <template #header-extra> {{ scheduled_time.toLocaleDateString()}} </template>
           <template #description> <div class="text-xs text-slate-300">
                {{ prop.lecture.id}}
           </div></template>
           <n-descriptions :column="1" label-placement="left">
            <n-descriptions-item label = "Time"> {{ scheduled_time.toLocaleTimeString() }}</n-descriptions-item>
            <n-descriptions-item label = "Streaming">
                <n-a :href = "prop.lecture.stream_url">Jump to Zoom</n-a>
            </n-descriptions-item>
            <n-descriptions-item label = "Recording">
                <n-a :href = "prop.lecture.recording_url">Jump to Zoom</n-a>
            </n-descriptions-item>
           </n-descriptions>
           <template #footer>
                <n-divider class="text-xs text-gray-400"> Attachments </n-divider>
                <n-space justify = "end" v-if="prop.isAdmin">
                    <n-popconfirm @positive-click="handleDelete">
                        <template #trigger>
                            <n-button  quaternary type = "error"> 
                                <template #icon>
                                    <n-icon>
                                        <delete />
                                    </n-icon>
                                </template> </n-button>
                        </template>
                        Are you sure you want to delete this lecture?
                    </n-popconfirm>
                </n-space>

           </template>
        </n-thing>
    </n-card>
</template>