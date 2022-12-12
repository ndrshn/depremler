<template>
  <a-row :gutter="[12, 12]">
    <a-col :span="24">
      <a-card size="small" title="Büyüklük Dağılımı">
        <LineChart v-bind="configLineMag" chart-ref="refLineMag" />
      </a-card>
    </a-col>
    <a-col :span="24">
      <a-card size="small" title="Aylık Dağılım">
        <LineChart v-bind="configLineDay" chart-ref="refLineDay" />
      </a-card>
    </a-col>
  </a-row>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { LineChart, ColumnChart } from "@opd/g2plot-vue";
import { Card as ACard, Col as ACol, Row as ARow } from "ant-design-vue";
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
const refLineMag = ref();
const refLineDay = ref();

const configLineMag = reactive({
  padding: true,
  xField: "mag",
  yField: "count",
  smooth: true,
  legend: {
    position: "top",
  },
  label: {
    position: "top",
  },
  data: [],
});

const configLineDay = reactive({
  padding: true,
  xField: "day",
  yField: "count",
  smooth: true,
  legend: {
    position: "top",
  },
  label: {
    position: "top",
  },
  data: [],
});

const populateData = () => {
  const groupedMag = _.groupBy(props.data, "mag");
  configLineMag.data = Object.keys(groupedMag)
    .map((el) => ({
      mag: el,
      count: groupedMag[el].length,
    }))
    .sort((a, b) => a.mag > b.mag);

  const groupedDate = _.groupBy(
    props.data.map((data) => ({ ...data, dayjs: dayjs(data.date).format("YYYY-MM-DD") })),
    "dayjs"
  );
  configLineDay.data = Object.keys(groupedDate).map((el) => ({
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
