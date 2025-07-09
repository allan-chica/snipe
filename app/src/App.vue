<template>

	<div class="container">
		<!-- Inputs -->
		<form @submit.prevent="searchJobs">
			<input type="text" name="keywords" placeholder="Keywords..." v-model="keywords">
			<div class="border"></div>
			<input class="location-input" type="text" name="location" placeholder="Location..." v-model="location">
			<div class="border"></div>
			<input class="timespan-input" type="number" name="time" placeholder="Time..." v-model="timespan">
			<div class="border"></div>
			<span class="input-group">
				<label for="remote">Remote?</label>
				<input type="checkbox" name="remote" id="remote" v-model="isRemote">
			</span>
			<!-- <div class="border"></div> -->
			<button type="submit">Submit</button>
		</form>

		<div v-if="isSearching">Searching...</div>

		<div v-else class="job-container">

			<h3 v-if="jobList.length == 0">Empty list :(</h3>

			<div v-else class="job-list">
				<div v-for="job in jobList" :key="job.job_id">
					<JobCard :job="job" @delete="deleteJob"/>
				</div>
			</div>

		</div>

	</div>

</template>

<script setup>
import { onMounted, ref } from 'vue'

// Component imports
import JobCard from './components/JobCard.vue'

const keywords = ref('')
const location = ref('')
const timespan = ref('')
const isRemote = ref(true)

const jobList = ref([])

const isSearching = ref(false)

const deletedJobs = ref([])

// Job data management
async function searchJobs() {
	const formatedKeywords = encodeURIComponent(keywords.value.toLowerCase())
	const formatedLocation = encodeURIComponent(location.value.toLowerCase())

	try {
		isSearching.value = true
		const res = await fetch(`/api/jobs
			?keywords=${formatedKeywords}
			&location=${formatedLocation}
			&timespan=${timespan.value}
			&remote=${isRemote.value}`)

		const data = await res.json()

		jobList.value = data.results
		jobList.value = jobList.value.filter(job => !deletedJobs.value.includes(job.job_id))
	} catch (e) {
		console.error(e)
	} finally {
		isSearching.value = false
	}
}

function deleteJob(id) {
	deletedJobs.value.push(id)
	localStorage.setItem('deleted', JSON.stringify(deletedJobs.value))
	jobList.value = jobList.value.filter(job => !deletedJobs.value.includes(job.job_id))
}

onMounted(() => {
	deletedJobs.value = JSON.parse(localStorage.getItem('deleted')) || []
})

</script>

<style scoped>

.location-input {
	width: 8rem;
}

.timespan-input {
	width: 5rem;
}

</style>
