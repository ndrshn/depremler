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
      <div class="row os-row">
        <div class="col-md-24" style="margin-bottom: 24px">
          <os-card>
            <div id="map" />
          </os-card>
        </div>
        <div class="col-md-24">
          <os-card :title="`${year} Depremleri`">
            <template #extra>
              <os-select size="small" v-model="year" @on-change="onChange">
                <os-option v-for="y in years" :value="y" :label="y" />
              </os-select>
            </template>
            <os-table
              v-if="data2003.length > 0"
              :data="data2003"
              :columns="columns"
              border
              pagination
              size="small"
              stripe
              style="width: 100%"
            >
              <template #bodyCell="{ record, column }">
                <template v-if="column.key === 'id'">
                  <os-tag color="info">{{ record.id }}</os-tag>
                </template>
                <template v-else>{{ record[column.key] }}</template>
              </template>
            </os-table>
          </os-card>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import OsTable from "./components/table.vue";
import data2003 from "../data/2003.json";
import OsTag from "./components/tag.vue";
import OsCard from "./components/card.vue";
import OsSelect from "./components/select.vue";
import OsOption from "./components/option.vue";

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

const columns = [
  {
    title: "id",
    key: "id",
    align: "center",
  },
  {
    title: "Location",
    key: "location",
  },
  {
    title: "Lat",
    key: "lat",
    align: "right",
  },
  {
    title: "Lng",
    key: "lng",
    align: "right",
  },
  {
    title: "Mag",
    key: "mag",
    align: "right",
  },
  {
    title: "Depth",
    key: "depth",
    align: "right",
  },
];

const onChange = (value) => {
  year.value = value;
};

onMounted(() => {
  map.value = L.map("map").setView([38.9637, 35.2433], 6);
  L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution: "",
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
