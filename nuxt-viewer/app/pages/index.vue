<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50">
      <div class="container mx-auto px-6 h-12 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-6 h-6 text-red-500 animate-pulse-logo"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke="currentColor"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M3 12h4l3 8l4 -16l3 8h4" />
          </svg>
          <span class="font-semibold">Earthquakes in Türkiye</span>
        </div>
        <UButton
          icon="i-lucide-sun"
          color="neutral"
          variant="ghost"
          aria-label="Toggle color mode"
          @click="$colorMode.preference = $colorMode.value === 'dark' ? 'light' : 'dark'"
        />
      </div>
    </header>

    <!-- Content -->
    <main class="container mx-auto px-6 py-6">
      <UTabs :items="tabs" :default-value="activeTab" @update:model-value="onTabChange">
        <template #data>
          <div class="space-y-6 mt-6">
            <!-- Map Card -->
            <UCard>
              <template #header>
                <div class="flex items-center gap-4">
                  <USelectMenu
                    v-model="selectedYear"
                    :items="years"
                    placeholder="Select Year"
                    class="w-32"
                    @update:model-value="loadData"
                  />
                  <span class="text-sm text-gray-500">{{ earthquakeCount }} earthquakes</span>
                </div>
              </template>
              <ClientOnly>
                <div id="map" />
              </ClientOnly>
            </UCard>

            <!-- Data Table Card -->
            <UCard>
              <template #header>
                <div class="flex items-center gap-4 flex-wrap">
                  <span class="text-sm text-gray-500">Filter in date:</span>
                  <input
                    type="date"
                    v-model="dateFrom"
                    class="px-3 py-1 border border-gray-300 dark:border-gray-700 rounded-md text-sm dark:bg-gray-800"
                    @change="loadData"
                  />
                  <span>-</span>
                  <input
                    type="date"
                    v-model="dateTo"
                    class="px-3 py-1 border border-gray-300 dark:border-gray-700 rounded-md text-sm dark:bg-gray-800"
                    @change="loadData"
                  />
                </div>
              </template>
              <UTable
                :data="paginatedData"
                :columns="columns"
                :loading="loading"
                class="w-full"
              />
              <template #footer>
                <div class="flex justify-center">
                  <UPagination
                    v-model="currentPage"
                    :total="filteredData.length"
                    :items-per-page="pageSize"
                  />
                </div>
              </template>
            </UCard>
          </div>
        </template>

        <template #statistics>
          <Statistics :data="filteredData" :year="selectedYear" v-if="activeTab === 'statistics'" class="mt-6" />
        </template>
      </UTabs>
    </main>
  </div>
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

const tabs = [
  { label: 'Data', value: 'data', slot: 'data' },
  { label: 'Statistics', value: 'statistics', slot: 'statistics' }
]

const activeTab = ref('data')
const onTabChange = (value: string) => {
  activeTab.value = value
}

const currentYear = new Date().getFullYear()
const years = Array(currentYear - 2002)
  .fill(null)
  .map((_, idx) => ({ label: String(2003 + idx), value: 2003 + idx }))

const selectedYear = ref<number>(2023)
const loading = ref(false)
const earthquakes = ref<Earthquake[]>([])
const dateFrom = ref(`${selectedYear.value}-01-01`)
const dateTo = ref(`${selectedYear.value}-12-31`)
const currentPage = ref(1)
const pageSize = 100

const filteredData = computed(() => {
  if (!dateFrom.value || !dateTo.value) return earthquakes.value
  return earthquakes.value.filter((d) => {
    const date = d.date.substring(0, 10)
    return date >= dateFrom.value && date <= dateTo.value
  })
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredData.value.slice(start, start + pageSize)
})

const earthquakeCount = computed(() => filteredData.value.length)

const columns = [
  { id: 'id', header: 'ID', accessorKey: 'id' },
  { id: 'date', header: 'Date', accessorKey: 'date' },
  { id: 'location', header: 'Location', accessorKey: 'location' },
  { id: 'lat', header: 'Lat', accessorKey: 'lat' },
  { id: 'lng', header: 'Lng', accessorKey: 'lng' },
  { id: 'mag', header: 'Mag', accessorKey: 'mag' },
  { id: 'depth', header: 'Depth', accessorKey: 'depth' }
]

// Leaflet types - will be dynamically imported
let L: any = null
let map: any = null
let layerControl: any = null
let levelLayers: Record<string, any> = {}

const getColor = (mag: number): number => {
  if (mag >= 0.0 && mag < 3) return 175
  else if (mag >= 3.0 && mag < 4.0) return 100
  else if (mag >= 4.0 && mag < 5.0) return 75
  else if (mag >= 5.0 && mag < 6.0) return 50
  else if (mag >= 6.0 && mag < 7.0) return 25
  else return 0
}

const findRange = (mag: number): string => {
  return `M${Math.floor(mag).toFixed(1)}-M${(Math.floor(mag) + 0.9).toFixed(1)}`
}

const renderData = () => {
  if (!map || !layerControl || !L) return

  Object.keys(levelLayers).forEach((el) => {
    levelLayers[el].clearLayers()
  })

  filteredData.value.forEach((el) => {
    const point = L.circle([el.lat, el.lng], {
      color: `hsl(${getColor(el.mag)} 100% 50%)`,
      fillOpacity: 0.8,
      radius: 50 * el.mag * el.mag
    })
    point.bindPopup(`${el.location}: M${el.mag} @ ${el.date}`)
    const range = findRange(el.mag)
    if (levelLayers[range]) {
      levelLayers[range].addLayer(point)
    }
  })

  Object.keys(levelLayers).forEach((el) => {
    layerControl.removeLayer(levelLayers[el])
    layerControl.addOverlay(levelLayers[el], el)
  })
}

const loadData = async () => {
  loading.value = true
  currentPage.value = 1
  
  dateFrom.value = `${selectedYear.value}-01-01`
  dateTo.value = `${selectedYear.value}-12-31`

  try {
    const response = await fetch(`/data/${selectedYear.value}.json`)
    earthquakes.value = await response.json()
    renderData()
  } catch (error) {
    console.error('Failed to load earthquake data:', error)
    earthquakes.value = []
  }

  loading.value = false
}

const initLegend = () => {
  if (!map || !L) return
  
  const legend = L.control({ position: 'bottomleft' })
  legend.onAdd = function () {
    const list = L.DomUtil.create('ul', 'legends')
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(175 100% 50%)"></i><span>M0.0-2.9</span></li>`
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(100 100% 50%)"></i><span>M3.0-3.9</span></li>`
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(75 100% 50%)"></i><span>M4.0-4.9</span></li>`
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(50 100% 50%)"></i><span>M5.0-5.9</span></li>`
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(25 100% 50%)"></i><span>M6.0-6.9</span></li>`
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(0 100% 50%)"></i><span>M7.0-7.9</span></li>`
    return list
  }
  legend.addTo(map)
}

const initMap = async () => {
  // Only run on client side
  if (import.meta.server) return
  
  // Dynamically import Leaflet on client side only
  const leaflet = await import('leaflet')
  L = leaflet.default || leaflet
  await import('leaflet/dist/leaflet.css')
  
  // Initialize layer groups after Leaflet is loaded
  levelLayers = {
    'M0.0-M0.9': L.layerGroup([]),
    'M1.0-M1.9': L.layerGroup([]),
    'M2.0-M2.9': L.layerGroup([]),
    'M3.0-M3.9': L.layerGroup([]),
    'M4.0-M4.9': L.layerGroup([]),
    'M5.0-M5.9': L.layerGroup([]),
    'M6.0-M6.9': L.layerGroup([]),
    'M7.0-M7.9': L.layerGroup([])
  }
  
  map = L.map('map').setView([38.9637, 35.2433], 6)
  L.tileLayer('https://cartodb-basemaps-b.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    maxZoom: 20
  }).addTo(map)

  layerControl = L.control.layers({}, {}).addTo(map)
  Object.keys(levelLayers).forEach((el) => {
    map.addLayer(levelLayers[el])
  })

  initLegend()
}

onMounted(async () => {
  await nextTick()
  await initMap()
  await loadData()
})

watch(filteredData, () => {
  renderData()
})
</script>
