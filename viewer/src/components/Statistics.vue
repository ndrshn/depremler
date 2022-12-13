<template>
  <a-row :gutter="[12, 12]">
    <a-col :span="4">
      <a-card size="small">
        <a-statistic :precision="1" title="Avg. Magnitude" prefix="M" :value="avgMag" />
      </a-card>
    </a-col>
    <a-col :span="4">
      <a-card size="small">
        <a-statistic :precision="1" title="Avg. Depth" prefix="KM" :value="avgDepth" />
      </a-card>
    </a-col>
    <a-col :span="4">
      <a-card size="small">
        <a-statistic
          :precision="0"
          title="Daily Avg."
          suffix="earthquakes"
          :value="props.data.length / 365"
        />
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card size="small">
        <a-statistic :precision="1" title="Highest Mag." prefix="M" :value="maxMag.mag">
          <template #suffix>
            <span style="font-size: 12px">
              {{
                `(${maxMag.earthquake.date} @ ${maxMag.earthquake.location} ${maxMag.earthquake.depth} KM)`
              }}
            </span>
          </template>
        </a-statistic>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card size="small">
        <a-statistic :precision="1" title="Deepest" prefix="KM" :value="maxDepth.depth">
          <template #suffix>
            <span style="font-size: 12px">
              {{
                `(${maxDepth.earthquake.date} @ ${maxDepth.earthquake.location} M${maxDepth.earthquake.mag})`
              }}
            </span>
          </template>
        </a-statistic>
      </a-card>
    </a-col>
    <a-col :span="12">
      <a-card size="small" title="Magnitude Dist.">
        <ColumnChart v-bind="configMag" />
      </a-card>
    </a-col>
    <a-col :span="12">
      <a-card size="small" title="Depth Dist.">
        <HistogramChart v-bind="configDepth" />
      </a-card>
    </a-col>
    <a-col :span="24">
      <a-card size="small" title="Daily Dist.">
        <ColumnChart v-bind="configDay" />
      </a-card>
    </a-col>
  </a-row>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { LineChart, ColumnChart, HistogramChart } from "@opd/g2plot-vue";
import {
  Card as ACard,
  Col as ACol,
  Row as ARow,
  Statistic as AStatistic,
} from "ant-design-vue";
import _ from "lodash";
import dayjs from "dayjs";
import "dayjs/locale/tr";

dayjs.locale("tr");

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});
const avgMag = ref(0);
const avgDepth = ref(0);

const maxMag = reactive({
  mag: -1,
  earthquake: {},
});

const maxDepth = reactive({
  depth: -1,
  earthquake: {},
});

const configMag = reactive({
  xField: "mag",
  yField: "count",
  label: {
    position: "top",
  },
  data: [],
});

const configDepth = reactive({
  binField: "depth",
  binWidth: 5,
  label: {
    position: "top",
  },
  data: [],
});

const configDay = reactive({
  xField: "day",
  yField: "count",
  label: {
    position: "top",
  },
  slider: {
    start: 0.0,
    end: 0.25,
  },
  data: [],
});

const populateData = () => {
  props.data.forEach((data) => {
    avgMag.value += data.mag;
    avgDepth.value += data.depth;
    if (data.mag > maxMag.mag) {
      maxMag.mag = data.mag;
      maxMag.earthquake = data;
    }
    if (data.depth > maxDepth.depth) {
      maxDepth.depth = data.depth;
      maxDepth.earthquake = data;
    }
  });
  avgMag.value = avgMag.value / props.data.length;
  avgDepth.value = avgDepth.value / props.data.length;

  configDepth.data = props.data;
  const groupedMag = _.groupBy(props.data, "mag");
  configMag.data = Object.keys(groupedMag)
    .map((el) => ({
      mag: el,
      count: groupedMag[el].length,
    }))
    .sort((a, b) => a.mag > b.mag);

  const groupedDate = _.groupBy(
    props.data.map((data) => ({ ...data, dayjs: dayjs(data.date).format("YYYY-MM-DD") })),
    "dayjs"
  );
  configDay.data = Object.keys(groupedDate).map((el) => ({
    day: el,
    count: groupedDate[el].length,
  }));
};

populateData();

watch(
  () => props.data,
  (newData) => {
    populateData();
  }
);
</script>

<style></style>
