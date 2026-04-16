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
import { computed } from "vue";
import { LineChart, ColumnChart, HistogramChart } from "@opd/g2plot-vue";
import {
  Card as ACard,
  Col as ACol,
  Row as ARow,
  Statistic as AStatistic,
} from "ant-design-vue";

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

// Single-pass aggregation: compute all derived values in one reduce
const stats = computed(() => {
  if (!props.data.length) {
    return {
      sumMag: 0,
      sumDepth: 0,
      maxMag: 0,
      maxMagEq: {},
      maxDepth: 0,
      maxDepthEq: {},
      magGroups: {},
      dayGroups: {},
    };
  }

  return props.data.reduce(
    (acc, d) => {
      acc.sumMag += d.mag;
      acc.sumDepth += d.depth;

      if (d.mag > acc.maxMag) {
        acc.maxMag = d.mag;
        acc.maxMagEq = d;
      }
      if (d.depth > acc.maxDepth) {
        acc.maxDepth = d.depth;
        acc.maxDepthEq = d;
      }

      const magKey = d.mag;
      acc.magGroups[magKey] = (acc.magGroups[magKey] || 0) + 1;

      const dayKey = d.date.substring(0, 10);
      acc.dayGroups[dayKey] = (acc.dayGroups[dayKey] || 0) + 1;

      return acc;
    },
    {
      sumMag: 0,
      sumDepth: 0,
      maxMag: -Infinity,
      maxMagEq: {},
      maxDepth: -Infinity,
      maxDepthEq: {},
      magGroups: {},
      dayGroups: {},
    }
  );
});

const avgMag = computed(() =>
  props.data.length ? stats.value.sumMag / props.data.length : 0
);

const avgDepth = computed(() =>
  props.data.length ? stats.value.sumDepth / props.data.length : 0
);

const maxMag = computed(() => ({
  mag: stats.value.maxMag === -Infinity ? 0 : stats.value.maxMag,
  earthquake: stats.value.maxMagEq,
}));

const maxDepth = computed(() => ({
  depth: stats.value.maxDepth === -Infinity ? 0 : stats.value.maxDepth,
  earthquake: stats.value.maxDepthEq,
}));

const configMag = computed(() => ({
  xField: "mag",
  yField: "count",
  label: { position: "top" },
  data: Object.keys(stats.value.magGroups)
    .map((mag) => ({ mag, count: stats.value.magGroups[mag] }))
    .sort((a, b) => (a.mag > b.mag ? 1 : -1)),
}));

const configDepth = computed(() => ({
  binField: "depth",
  binWidth: 5,
  label: { position: "top" },
  data: props.data,
}));

const configDay = computed(() => ({
  xField: "day",
  yField: "count",
  label: { position: "top" },
  slider: { start: 0.0, end: 0.25 },
  data: Object.keys(stats.value.dayGroups).map((day) => ({
    day,
    count: stats.value.dayGroups[day],
  })),
}));
</script>

<style></style>
