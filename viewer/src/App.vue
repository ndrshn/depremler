<template>
  <div class="container">
    <header class="header">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="icon icon-tabler icon-tabler-activity logo"
        width="24"
        height="24"
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
    </header>
    <section class="content">
      <a-row :gutter="[24, 24]">
        <a-col :span="24">
          <a-card size="small">
            <div id="map" />
          </a-card>
        </a-col>
        <a-col :span="24">
          <a-card :title="`${year} Depremleri (${data.length} deprem)`" size="small">
            <template #extra>
              <a-select
                v-model:value="year"
                style="width: 120px"
                size="small"
                @change="loadData"
              >
                <a-select-option v-for="y in years" :key="y" :value="y">{{
                  y
                }}</a-select-option>
              </a-select>
            </template>
            <a-table
              :data-source="data"
              :columns="columns"
              bordered
              :pagination="{ pageSize: 100 }"
              size="small"
            />
          </a-card>
        </a-col>
      </a-row>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  Table as ATable,
  Card as ACard,
  Select as ASelect,
  SelectOption as ASelectOption,
  Col as ACol,
  Row as ARow,
} from "ant-design-vue";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const years = [
  2003,
  2004,
  2005,
  2006,
  2007,
  2008,
  2009,
  2010,
  2011,
  2012,
  2013,
  2014,
  2015,
  2016,
  2017,
  2018,
  2019,
  2020,
  2021,
  2022,
];

const year = ref(2003);
const map = ref();
const data = ref([]);
const loading = ref(false);

const columns = [
  {
    title: "id",
    key: "id",
    dataIndex: "id",
    align: "center",
    width: 100,
  },
  {
    title: "Location",
    key: "location",
    dataIndex: "location",
  },
  {
    title: "Lat",
    key: "lat",
    dataIndex: "lat",
    align: "right",
  },
  {
    title: "Lng",
    key: "lng",
    dataIndex: "lng",
    align: "right",
  },
  {
    title: "Mag",
    key: "mag",
    dataIndex: "mag",
    align: "right",
  },
  {
    title: "Depth",
    key: "depth",
    dataIndex: "depth",
    align: "right",
  },
];

const loadData = async (value) => {
  loading.value = true;
  await import(`../data/${value}.json`).then((res) => {
    data.value = res.default;
  });
  loading.value = false;

  data.value.forEach((el) => {
    const point = L.circle([el.lat, el.lng], {
      color: `hsl(${(8 - el.mag) * 180}, 100%, 50%)`,
      fillOpacity: 0.9,
      radius: 200 * el.mag,
    }).addTo(map.value);
    point.bindPopup(`${el.location}: M${el.mag} @ ${el.date}`);
  });
};
loadData(year.value);
onMounted(() => {
  map.value = L.map("map").setView([38.9637, 35.2433], 6);
  L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution: "...",
    maxZoom: 18,
  }).addTo(map.value);
});
</script>

<style scoped>
.container {
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
  width: 100%;
  height: 100%;
}

.header {
  background-color: #fff;
  width: 100%;
  height: 40px;
  display: flex;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  justify-content: space-between;
  align-items: center;
  align-content: center;
  border-bottom: 1px solid #ececec;
  padding: 0 24px;
}

.logo {
  width: 24px;
  height: 24px;
  stroke-width: 1.25;
  stroke: #e56257;
  transition: all 0.15s ease 0s;
  -webkit-animation: tada-keyframes 3s ease infinite;
  animation: tada-keyframes 3s ease infinite;
  animation-fill-mode: none;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

.content {
  width: 100%;
  min-height: calc(100vh - 40px);
  height: auto;
  padding: 24px;
  z-index: 1;
}

@-webkit-keyframes tada-keyframes {
  0% {
    transform: scale3d(1, 1, 1);
  }

  10%,
  5% {
    transform: scale3d(0.9, 0.9, 0.9) rotate3d(0, 0, 1, -5deg);
  }

  15%,
  25%,
  35%,
  45% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, 5deg);
  }

  20%,
  30%,
  40% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, -5deg);
  }

  50% {
    transform: scale3d(1, 1, 1);
  }
}

@keyframes tada-keyframes {
  0% {
    transform: scale3d(1, 1, 1);
  }

  10%,
  5% {
    transform: scale3d(0.9, 0.9, 0.9) rotate3d(0, 0, 1, -5deg);
  }

  15%,
  25%,
  35%,
  45% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, 5deg);
  }

  20%,
  30%,
  40% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, -5deg);
  }

  50% {
    transform: scale3d(1, 1, 1);
  }
}

#map {
  width: 100%;
  height: 640px;
}
</style>
