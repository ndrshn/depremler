<!-- eslint-disable no-unused-vars -->
<template>
  <ul
    v-if="props.simple"
    class="os-pagination os-pagination--simple"
    :class="{
      [`os-pagination--${props.size}`]: props.size,
    }"
  >
    <li
      title="Önceki"
      class="os-pagination__prev"
      :class="{
        'os-pagination--disabled': currentPage === 1,
        'os-pagination--circle': props.circle,
      }"
      @click="handlePrev"
    >
      <i class="icon ti ti-chevron-left"></i>
    </li>
    <div class="os-pagination__simple-paging">
      <input
        type="text"
        class="os-input__original"
        :value="currentPage"
        @keydown="handleKeydown"
        @keyup="handleKeyup"
        @change="handleKeyup"
      />
      <span>/</span>
      <span class="os-pagination__paging-total">{{ totalPage }}</span>
    </div>
    <li
      title="Sonraki"
      class="os-pagination__next"
      :class="{
        'os-pagination--disabled': currentPage === totalPage,
      }"
      @click="handleNext"
    >
      <i class="icon ti ti-chevron-right"></i>
    </li>
  </ul>
  <ul
    v-else
    class="os-pagination"
    :class="{
      [`os-pagination--${props.size}`]: props.size,
    }"
  >
    <span v-show="showTotal" class="os-pagination__total">
      <slot name="total">{{ `toplam ${props.total} kayıt` }}</slot>
    </span>
    <li
      title="Önceki"
      class="os-pagination__prev"
      :class="{
        'os-pagination--disabled': currentPage === 1,
        'os-pagination--circle': props.circle,
      }"
      @click="handlePrev"
    >
      <i class="icon ti ti-chevron-left"></i>
    </li>
    <template v-if="totalPage < 9">
      <li
        v-for="num in pageRange"
        :key="num"
        class="os-pagination__item"
        :class="{
          'os-pagination__item--active': currentPage === num,
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(num)"
      >
        {{ num }}
      </li>
    </template>
    <template v-else>
      <li
        class="os-pagination__item"
        :class="{
          'os-pagination__item--active': currentPage === 1,
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(1)"
      >
        1
      </li>
      <li
        v-if="currentPage > 4"
        class="os-pagination__item os-pagination__item--jump-prev"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        title="Önceki"
        @click="handleJumpPrev"
      >
        <i class="icon ti ti-chevrons-left"></i>
      </li>
      <li
        v-if="currentPage > 3"
        class="os-pagination__item"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(currentPage - 2)"
      >
        {{ currentPage - 2 }}
      </li>
      <li
        v-if="currentPage > 2"
        class="os-pagination__item"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(currentPage - 1)"
      >
        {{ currentPage - 1 }}
      </li>
      <li
        v-if="currentPage !== 1 && currentPage !== totalPage"
        class="os-pagination__item os-pagination__item--active"
        :class="{
          'os-pagination--circle': props.circle,
        }"
      >
        {{ currentPage }}
      </li>
      <li
        v-if="currentPage < totalPage - 1"
        class="os-pagination__item"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(currentPage + 1)"
      >
        {{ currentPage + 1 }}
      </li>
      <li
        v-if="currentPage < totalPage - 2"
        class="os-pagination__item"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(currentPage + 2)"
      >
        {{ currentPage + 2 }}
      </li>
      <li
        v-if="currentPage < totalPage - 3"
        class="os-pagination__item os-pagination__item--jump-next"
        :class="{
          'os-pagination--circle': props.circle,
        }"
        title="Sonraki"
        @click="handleJumpNext"
      >
        <i class="icon ti ti-chevrons-right"></i>
      </li>
      <li
        v-if="totalPage > 1"
        class="os-pagination__item"
        :class="{
          'os-pagination__item--active': currentPage === totalPage,
          'os-pagination--circle': props.circle,
        }"
        @click="changePage(totalPage)"
      >
        {{ totalPage }}
      </li>
    </template>
    <li
      title="Sonraki"
      class="os-pagination__next"
      :class="{
        'os-pagination--disabled': currentPage === totalPage,
        'os-pagination--circle': props.circle,
      }"
      @click="handleNext"
    >
      <i class="icon ti ti-chevron-right"></i>
    </li>
    <div v-if="props.showQuickjump" class="os-pagination__quickjump">
      <span>Git</span>
      <input
        v-model="jumpPageNum"
        type="text"
        class="os-input__original"
        @keydown="handleKeydown"
        @keyup.enter="changePage()"
      />
      <span>Sayfa</span>
    </div>
  </ul>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const emit = defineEmits(["page-change", "pagesize-change"]);
const props = defineProps({
  current: {
    type: Number,
    default: 1,
  },
  total: {
    type: Number,
    required: true,
    default: 0,
  },
  pageSize: {
    type: Number,
    default: 100,
  },
  size: {
    type: String,
    default: "normal",
  },
  simple: {
    type: Boolean,
    default: false,
  },
  showTotal: {
    type: Boolean,
    default: false,
  },
  showQuickjump: {
    type: Boolean,
    default: false,
  },
  showSizer: {
    type: Boolean,
    default: false,
  },
  circle: {
    type: Boolean,
    default: false,
  },
  pageSizeOpts: {
    type: Array,
    default() {
      return [10, 20, 30, 40];
    },
  },
});

const currentPage = ref(props.current);
const currentPageSize = ref(props.pageSize);
const jumpPageNum = ref(props.current);

const totalPage = computed(() => {
  const num = Math.ceil(props.total / currentPageSize.value);
  return num === 0 ? 1 : num;
});

const visiblePage = computed(() => {
  return totalPage.value >= 5 ? 5 : totalPage.value;
});

const pageRange = computed(() => {
  const range = [];
  let start = 1;

  if (currentPage.value + visiblePage.value / 2 > totalPage.value) {
    start = totalPage.value - visiblePage.value + 1;
    start = start > 0 ? start : 1;
  } else if (currentPage.value - visiblePage.value / 2 > 0) {
    start = Math.ceil(currentPage.value - visiblePage.value / 2);
  }

  for (let i = 0; i < visiblePage.value && i < totalPage.value; i++) {
    range.push(start + i);
  }

  return range;
});

const changePage = (page) => {
  let num = (page || jumpPageNum.value || 1) | 0;
  num = num > totalPage.value ? totalPage.value : num;
  num = num < 1 ? 1 : num;

  if (currentPage.value !== num) {
    jumpPageNum.value = num;
    currentPage.value = num;
    emit("page-change", num);
  }
};

const handlePrev = () => {
  if (currentPage.value <= 1) return false;
  changePage(currentPage.value - 1);
};

const handleNext = () => {
  if (currentPage.value >= totalPage.value) return false;
  changePage(currentPage.value + 1);
};

const handleJumpPrev = () => {
  const page = currentPage.value - 5;
  page ? changePage(page) : changePage(1);
};

const handleJumpNext = () => {
  const page = currentPage.value + 5;
  page > totalPage.value ? changePage(totalPage.value) : changePage(page);
};

const handleKeydown = (evt) => {
  const key = evt.keyCode;
  if (!((key >= 48 && key <= 57) || key === 8 || key === 37 || key === 39)) {
    evt.preventDefault();
  }
};

const handleKeyup = (evt) => {
  const key = evt.keyCode;
  const numVal = evt.target.value | 0;
  if (key === 40) {
    // Up Arrow
    this.handlePrev();
  } else if (key === 38) {
    // Down Arrow
    this.handleNext();
  } else if (key === 13) {
    // Return
    let page = 1;

    page = numVal > totalPage.value ? totalPage.value : numVal;
    page = numVal <= 0 ? 1 : numVal;
    evt.target.value = page;
    changePage(page);
  }
};

const changeSize = (size) => {
  currentPageSize.value = size;
  changePage(1);
  emit("pagesize-change", size);
};

watch(
  () => props.current,
  (newVal) => {
    currentPage.value = newVal;
  }
);

watch(
  () => props.pageSize,
  (newVal) => {
    currentPageSize.value = newVal;
  }
);
</script>

<style>
.os-pagination {
  list-style: none;
  font-size: 0;
  padding: 0;
  display: inline-flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}

.os-pagination:after {
  clear: both;
  content: "";
  display: block;
}

.os-pagination__item,
.os-pagination__prev,
.os-pagination__next,
.os-pagination__item--jump-prev,
.os-pagination__item--jump-next {
  float: left;
  min-width: 24px;
  height: 24px;
  color: #3f536e;
  font-size: 11px;
  line-height: 24px;
  text-align: center;
  border: 1px solid #c5d9e8;
  border-radius: 4px;
  background-color: #fff;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  cursor: pointer;
}

.os-pagination__item:hover,
.os-pagination__prev:hover,
.os-pagination__next:hover,
.os-pagination__item--jump-prev:hover,
.os-pagination__item--jump-next:hover {
  color: #79a1eb;
  border-color: #79a1eb;
}

.os-pagination--circle {
  border-radius: 50%;
}

.os-pagination__item + .os-pagination__item {
  margin-left: 4px;
}

.os-pagination__item--active {
  color: #fff;
  border-color: #79a1eb;
  background-color: #79a1eb;
}

.os-pagination__item--active:hover {
  color: #fff;
}

.os-pagination__prev {
  margin-right: 8px;
}

.os-pagination__next {
  margin-left: 8px;
}

.os-pagination__item--jump-prev:after,
.os-pagination__item--jump-next:after {
  content: "\2022\2022\2022";
  display: inline-block;
  color: #ececec;
  font-size: 8px;
  text-align: center;
  line-height: 28px;
  letter-spacing: 1px;
}

.os-pagination__item--jump-prev i,
.os-pagination__item--jump-next i {
  display: none;
}

.os-pagination__item--jump-prev:hover:after,
.os-pagination__item--jump-next:hover:after {
  display: none;
}

.os-pagination__item--jump-prev:hover i,
.os-pagination__item--jump-next:hover i {
  display: inline-block;
}

.os-pagination__total {
  float: left;
  height: 28px;
  font-size: 12px;
  line-height: 28px;
  margin-right: 12px;
}

.os-pagination__quickjump {
  float: left;
  margin-left: 12px;
  font-size: 12px;
  line-height: 28px;
}

.os-pagination__quickjump input {
  display: inline-block;
  margin: 0 8px;
  width: 40px;
  height: 28px;
  text-align: center;
  line-height: 28px;
}

.os-pagination__sizer {
  float: left;
  margin-left: 12px;
  text-align: center;
}

.os-pagination__simple-paging {
  float: left;
  font-size: 12px;
}

.os-pagination__simple-paging input {
  display: inline-block;
  padding: 2px 4px;
  width: 28px;
  height: 28px;
  text-align: center;
  line-height: 28px;
}

.os-pagination__simple-paging span {
  padding: 0 4px;
}

.os-pagination--disabled {
  color: #ececec;
  border-color: #ececec;
  cursor: not-allowed;
}

.os-pagination--disabled:hover {
  color: #ececec;
  border-color: #ececec;
}

.os-pagination--small .os-pagination__total,
.os-pagination--small .os-pagination__quickjump,
.os-pagination--small .os-pagination__item,
.os-pagination--small .os-pagination__prev,
.os-pagination--small .os-pagination__next {
  height: 20px;
  font-size: 11px;
  line-height: 20px;
}

.os-pagination--small .os-pagination__item,
.os-pagination--small .os-pagination__prev,
.os-pagination--small .os-pagination__next {
  border: none;
  width: 20px;
  min-width: 20px;
}

.os-pagination--small .os-pagination__item--jump-prev:after,
.os-pagination--small .os-pagination__item--jump-next:after {
  font-size: 7px;
  line-height: 20px;
}

.os-pagination--small .os-pagination__total {
  margin-right: 8px;
}

.os-pagination--small .os-pagination__sizer {
  margin-left: 8px;
}

.os-pagination--small .os-pagination__sizer .os-select .os-select__selection {
  height: 20px;
  line-height: 18px;
}

.os-pagination--small .os-pagination__quickjump {
  margin-left: 8px;
}

.os-pagination--small .os-pagination__quickjump .os-input__original {
  margin: 0 6px;
  height: 20px;
  font-size: 11px;
}

.os-pagination--simple {
  font-size: 12px;
}

.os-pagination--simple .os-input__original {
  margin: 0 4px;
  width: 32px;
  height: 28px;
}

.os-pagination--simple .os-pagination__prev,
.os-pagination--simple .os-pagination__next {
  margin: 0;
  border: none;
  width: 28px;
  min-width: 28px;
  height: 28px;
  line-height: 28px;
}

.os-pagination--simple.os-pagination--small {
  font-size: 11px;
}

.os-pagination--simple.os-pagination--small .os-input__original {
  width: 26px;
  height: 20px;
}

.os-pagination--simple.os-pagination--small .os-input__original input {
  font-size: 11px;
}

.os-pagination--simple.os-pagination--small .os-pagination__prev,
.os-pagination--simple.os-pagination--small .os-pagination__next {
  width: 20px;
  min-width: 20px;
  height: 20px;
  line-height: 20px;
}

.os-pagination--simple.os-pagination--small .os-pagination__simple-paging {
  font-size: 11px;
}

.os-pagination--simple.os-pagination--small .os-pagination__simple-paging span {
  padding: 0 4px;
}

/* input */
</style>
