<template>
	<div class="job-card" :class="{ 'applied': hasApplied }">

		<div class="job-header">
			<h2>{{ job.title }}</h2>
			<span> - {{ job.job_id }}</span>
		</div>

		<div class="job-body">
			<p><span class="job-location">{{ job.location }}</span><span v-if="job.company"> - {{ job.company }}</span></p>
			<p class="job-time">{{ job.posted }}</p>
		</div>

		<div class="job-actions">

			<button class="btn-apply" :class="{ 'applied': hasApplied }" @click="apply">
				{{ !hasApplied ? 'Apply' : 'Applied' }}
			</button>

			<button class="btn-delete" @click="$emit('delete', job.job_id)">Delete</button>
		</div>

	</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
	job: {
		type: Object,
		required: true
	}
})

defineEmits(['delete'])

const hasApplied = ref(false)
const applied = ref([])

function apply() {
	window.open(props.job.url, '_blank').focus()

	applied.value.push(props.job.job_id)
	localStorage.setItem('applied', JSON.stringify(applied.value))
	hasApplied.value = true
}

onMounted(() => {
	applied.value = JSON.parse(localStorage.getItem('applied')) || []

	if (applied.value.length != 0 && applied.value.includes(props.job.job_id)) {
		hasApplied.value = true
	}
})

</script>

<style scoped>

.job-card {
	border-bottom: 1px solid rgb(187, 187, 187);
	padding: 1rem 0;
	position: relative;
}

.job-header h2 {
	font-weight: 600;
	display: inline;
}

.job-header span {
	color: grey;
}

.applied .job-header,
.applied .job-body {
	opacity: 50%;
}

.job-body {
	font-family: 'Montserrat';
}

.job-location {
	font-weight: 600;
}

.job-time {
	color: grey;
}

.job-actions {
	position: absolute;
	right: 0;
	bottom: 1rem;
	display: flex;
	gap: 0.5rem;
}

.job-actions button {
	background-color: transparent;
	border: 1px solid;
	outline: none;
	font-family: 'Montserrat', sans-serif;
	cursor: pointer;
	padding: 0.45rem 0.5rem;
}

.job-actions .btn-apply {
	border-color: black;
	background-color: black;
	color: white;
}

.job-actions .btn-apply:hover {
	background-color: rgb(56, 56, 56);
}

.job-actions .btn-apply.applied {
	background-color: transparent;
	color: black;
}

.job-actions .btn-delete {
	border-color: red;
	color: #ff6666;
}

.job-actions .btn-delete:hover {
	background-color: #ff6666;
	color: white;
}

</style>