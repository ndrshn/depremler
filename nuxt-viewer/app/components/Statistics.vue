<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Average Magnitude -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Avg. Magnitude</div>
        <div class="text-3xl font-bold text-primary">M{{ avgMag.toFixed(1) }}</div>
      </div>
    </UCard>

    <!-- Average Depth -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Avg. Depth</div>
        <div class="text-3xl font-bold text-primary">{{ avgDepth.toFixed(1) }} KM</div>
      </div>
    </UCard>

    <!-- Daily Average -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Daily Avg.</div>
        <div class="text-3xl font-bold text-primary">{{ dailyAvg.toFixed(0) }}</div>
        <div class="text-xs text-gray-400">earthquakes</div>
      </div>
    </UCard>

    <!-- Highest Magnitude -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Highest Mag.</div>
        <div class="text-3xl font-bold text-red-500">M{{ maxMag.mag.toFixed(1) }}</div>
        <div class="text-xs text-gray-400 truncate" v-if="maxMag.earthquake">
          {{ maxMag.earthquake.date }} @ {{ maxMag.earthquake.location }}
        </div>
      </div>
    </UCard>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
    <!-- Deepest -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Deepest</div>
        <div class="text-3xl font-bold text-blue-500">{{ maxDepth.depth.toFixed(1) }} KM</div>
        <div class="text-xs text-gray-400 truncate" v-if="maxDepth.earthquake">
          {{ maxDepth.earthquake.date }} @ {{ maxDepth.earthquake.location }} M{{ maxDepth.earthquake.mag }}
        </div>
      </div>
    </UCard>

    <!-- Total -->
    <UCard>
      <div class="text-center">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Earthquakes in {{ year }}</div>
        <div class="text-3xl font-bold text-primary">{{ props.data.length }}</div>
      </div>
    </UCard>
  </div>

  <!-- Magnitude Distribution -->
  <UCard class="mt-4">
    <template #header>
      <h3 class="font-semibold">Magnitude Distribution</h3>
    </template>
    <div class="grid grid-cols-4 md:grid-cols-8 gap-2">
      <div 
        v-for="item in magDistribution" 
        :key="item.range"
        class="text-center p-3 rounded-lg"
        :style="{ backgroundColor: `hsl(${item.color} 100% 50% / 0.2)` }"
      >
        <div class="text-xs text-gray-500 dark:text-gray-400">{{ item.range }}</div>
        <div class="text-lg font-bold" :style="{ color: `hsl(${item.color} 100% 40%)` }">
          {{ item.count }}
        </div>
      </div>
    </div>
  </UCard>

  <!-- Depth Distribution -->
  <UCard class="mt-4">
    <template #header>
      <h3 class="font-semibold">Depth Distribution</h3>
    </template>
    <div class="grid grid-cols-4 md:grid-cols-6 gap-2">
      <div 
        v-for="item in depthDistribution" 
        :key="item.range"
        class="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg"
      >
        <div class="text-xs text-gray-500 dark:text-gray-400">{{ item.range }}</div>
        <div class="text-lg font-bold text-blue-600 dark:text-blue-400">{{ item.count }}</div>
      </div>
    </div>
  </UCard>

  <!-- Monthly Distribution -->
  <UCard class="mt-4">
    <template #header>
      <h3 class="font-semibold">Monthly Distribution</h3>
    </template>
    <div class="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-2">
      <div 
        v-for="item in monthlyDistribution" 
        :key="item.month"
        class="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
      >
        <div class="text-xs text-gray-500 dark:text-gray-400">{{ item.month }}</div>
        <div class="text-lg font-bold text-primary">{{ item.count }}</div>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
interface Earthquake {
  id: number
  date: string
  location: string
  lat: number
  lng: number
  mag: number
  depth: number
}

const props = defineProps<{
  data: Earthquake[]
  year: number
}>()

const avgMag = computed(() => {
  if (props.data.length === 0) return 0
  return props.data.reduce((sum, d) => sum + d.mag, 0) / props.data.length
})

const avgDepth = computed(() => {
  if (props.data.length === 0) return 0
  return props.data.reduce((sum, d) => sum + d.depth, 0) / props.data.length
})

const dailyAvg = computed(() => {
  // Calculate days in year (account for leap years)
  const isLeapYear = (props.year % 4 === 0 && props.year % 100 !== 0) || (props.year % 400 === 0)
  const daysInYear = isLeapYear ? 366 : 365
  return props.data.length / daysInYear
})

const maxMag = computed(() => {
  if (props.data.length === 0) return { mag: 0, earthquake: null }
  const max = props.data.reduce((max, d) => (d.mag > max.mag ? d : max), props.data[0])
  return { mag: max.mag, earthquake: max }
})

const maxDepth = computed(() => {
  if (props.data.length === 0) return { depth: 0, earthquake: null }
  const max = props.data.reduce((max, d) => (d.depth > max.depth ? d : max), props.data[0])
  return { depth: max.depth, earthquake: max }
})

const getColorForMag = (mag: number): number => {
  if (mag >= 0 && mag < 3) return 175
  else if (mag >= 3 && mag < 4) return 100
  else if (mag >= 4 && mag < 5) return 75
  else if (mag >= 5 && mag < 6) return 50
  else if (mag >= 6 && mag < 7) return 25
  else return 0
}

const magDistribution = computed(() => {
  const ranges = [
    { range: 'M0-1', min: 0, max: 1, color: 175 },
    { range: 'M1-2', min: 1, max: 2, color: 175 },
    { range: 'M2-3', min: 2, max: 3, color: 175 },
    { range: 'M3-4', min: 3, max: 4, color: 100 },
    { range: 'M4-5', min: 4, max: 5, color: 75 },
    { range: 'M5-6', min: 5, max: 6, color: 50 },
    { range: 'M6-7', min: 6, max: 7, color: 25 },
    { range: 'M7+', min: 7, max: 10, color: 0 }
  ]

  return ranges.map((r) => ({
    ...r,
    count: props.data.filter((d) => d.mag >= r.min && d.mag < r.max).length
  }))
})

const depthDistribution = computed(() => {
  const ranges = [
    { range: '0-10km', min: 0, max: 10 },
    { range: '10-20km', min: 10, max: 20 },
    { range: '20-50km', min: 20, max: 50 },
    { range: '50-100km', min: 50, max: 100 },
    { range: '100-200km', min: 100, max: 200 },
    { range: '200km+', min: 200, max: 1000 }
  ]

  return ranges.map((r) => ({
    ...r,
    count: props.data.filter((d) => d.depth >= r.min && d.depth < r.max).length
  }))
})

const monthlyDistribution = computed(() => {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  
  return months.map((month, idx) => {
    const monthNum = String(idx + 1).padStart(2, '0')
    const count = props.data.filter((d) => {
      const dateMonth = d.date.substring(5, 7)
      return dateMonth === monthNum
    }).length
    return { month, count }
  })
})
</script>
