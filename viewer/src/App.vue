<template>
  <div class="container">
    <header class="header">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-activity logo" width="24" height="24"
        viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
        stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M3 12h4l3 8l4 -16l3 8h4" />
      </svg>
      <span>Earthquakes in Türkiye</span>
    </header>
    <section class="content">
      <a-tabs v-model:activeKey="activeKey" type="card">
        <a-tab-pane key="1" tab="Data">
          <a-row :gutter="[24, 24]">
            <a-col :span="24">
              <a-card size="small">
                <div id="map" />
              </a-card>
            </a-col>
            <a-col :span="24">
              <a-card size="small">
                <a-table :data-source="data" :columns="columns" bordered :loading="loading"
                  :pagination="{ pageSize: 100, size: 'small' }" size="small">
                  <template #title>
                    <a-space>
                      <a-select v-model:value="year" style="width: 100%" size="small" @change="loadData">
                        <a-select-option v-for="y in years" :key="y" :value="y">{{
                          y
                        }}</a-select-option>
                      </a-select>
                      <span>{{ data.length }} earthquakes. Filter in date:</span>
                      <a-range-picker v-model:value="range" @change="loadData" size="small" :bordered="false" />
                    </a-space>
                  </template>
                </a-table>
              </a-card>
            </a-col>
          </a-row>
        </a-tab-pane>
        <a-tab-pane key="2" :tab="`Statistics for ${year}`" :disabled="loading">
          <Statistics :data="data" v-if="activeKey === '2'" />
        </a-tab-pane>
      </a-tabs>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from "vue";
import {
  Button as AButton,
  Table as ATable,
  Card as ACard,
  Select as ASelect,
  SelectOption as ASelectOption,
  Col as ACol,
  Row as ARow,
  Space as ASpace,
  Tabs as ATabs,
  TabPane as ATabPane,
  RangePicker as ARangePicker,
} from "ant-design-vue";
import dayjs from "dayjs";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import Statistics from "./components/Statistics.vue";

const activeKey = ref("1");

const years = Array(new Date().getFullYear() - 2002)
  .fill()
  .map((_, idx) => 2003 + idx);

const year = ref(2003);
const map = ref();
const data = ref([]);
const loading = ref(false);
const range = ref([dayjs(`${year.value}-01-01`), dayjs(`${year.value}-12-31`)]);
const levelLayers = reactive({
  "M0.0-M0.9": L.layerGroup([]),
  "M1.0-M1.9": L.layerGroup([]),
  "M2.0-M2.9": L.layerGroup([]),
  "M3.0-M3.9": L.layerGroup([]),
  "M4.0-M4.9": L.layerGroup([]),
  "M5.0-M5.9": L.layerGroup([]),
  "M6.0-M6.9": L.layerGroup([]),
  "M7.0-M7.9": L.layerGroup([]),
});
const layerControl = ref();
const columns = [
  {
    title: "id",
    key: "id",
    dataIndex: "id",
    align: "center",
    width: 100,
  },
  {
    title: "Date",
    key: "date",
    dataIndex: "date",
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

const getColor = (mag) => {
  if (mag >= 0.0 && mag < 3) return 175;
  else if (mag >= 3.0 && mag < 4.0) return 100;
  else if (mag >= 4.0 && mag < 5.0) return 75;
  else if (mag >= 5.0 && mag < 6.0) return 50;
  else if (mag >= 6.0 && mag < 7.0) return 25;
  else return 0;
};

const findRange = (mag) => {
  return `M${Math.floor(mag).toFixed(1)}-M${(Math.floor(mag) + 0.9).toFixed(1)}`;
};

const renderData = () => {
  Object.keys(levelLayers).forEach((el) => {
    levelLayers[el].clearLayers();
  });
  data.value.forEach((el) => {
    const point = L.circle([el.lat, el.lng], {
      color: `hsl(${getColor(el.mag)} 100% 50%)`,
      fillOpacity: 0.8,
      radius: 50 * el.mag * el.mag,
      zIndexOffset: Math.ceil(el.mag) * 10,
    });
    point.bindPopup(`${el.location}: M${el.mag} @ ${el.date}`);
    levelLayers[findRange(el.mag)].addLayer(point);
  });
  Object.keys(levelLayers).forEach((el) => {
    layerControl.value.removeLayer(levelLayers[el]);
    layerControl.value.addOverlay(levelLayers[el], el);
  });
};

const loadData = async () => {
  loading.value = true;
  range.value[0] = range.value[0].year(year.value);
  range.value[1] = range.value[1].year(year.value);
  const from = range.value[0];
  const to = range.value[1];
  await import(`../data/${year.value}.json`).then((res) => {
    data.value = res.default;
  });
  data.value = data.value.filter((d) => dayjs(d.date) >= from && dayjs(d.date) <= to);
  renderData();
  loading.value = false;
};

loadData(year.value);

const initLegend = () => {
  var legend = L.control({ position: "bottomleft" });
  legend.onAdd = function (map) {
    const list = L.DomUtil.create("ul", "legend");
    list.className = "legends";
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(175 100% 50%)"></i><span>M0.0-2.9</span></li>`;
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(100 100% 50%)"></i><span>M3.0-3.9</span></li>`;
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(75 100% 50%)"></i><span>M4.0-4.9</span></li>`;
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(50 100% 50%)"></i><span>M5.0-5.9</span></li>`;
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(25 100% 50%)"></i><span>M6.0-6.9</span></li>`;
    list.innerHTML += `<li class="legend"><i style="background-color: hsl(0 100% 50%)"></i><span>M7.0-7.9</span></li>`;
    return list;
  };
  legend.addTo(map.value);
};

onMounted(() => {
  map.value = L.map("map").setView([38.9637, 35.2433], 6);
  L.tileLayer(
    "https://cartodb-basemaps-b.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
    {
      tileset_id: "mapbox.mapbox-streets-v8,mapbox.mapbox-terrain-v2",
      attribution: "...",
      maxZoom: 20,
    }
  ).addTo(map.value);
  layerControl.value = L.control.layers({}, {}).addTo(map.value);
  Object.keys(levelLayers).forEach((el) => {
    map.value.addLayer(levelLayers[el]);
  });
  initLegend();
});
</script>

<style>
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

.legends {
  padding: 0 6px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  list-style: none;
  display: flex;
  flex-direction: column;
}

.legends .legend {
  margin-bottom: 3px;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.legends span {
  color: #eee;
}

.legends i {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  float: left;
  opacity: 0.7;
}

#map,
.ant-card,
.ant-input,
.ant-select:not(.ant-select-customize-input) .ant-select-selector,
.ant-pagination-item {
  border-radius: 5px;
}

.ant-input-search>.ant-input-group>.ant-input-group-addon:last-child .ant-input-search-button {
  border-radius: 0 5px 5px 0;
}

.ant-table-title {
  border-radius: 5px 5px 0 0;
}
</style>
