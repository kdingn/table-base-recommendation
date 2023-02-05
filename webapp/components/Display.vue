<template>
  <div>
    <b-card class="mx-3 mt-2" bg-variant="dark">
      <font color="white">
        <b-container class="float-left">
          <h3>
              Search Box
          </h3>
          <b-row class="float-left">
            <b-col>
              ⚙ DatasetType<br>
              <b-form-select
                v-model="contentsToShow"
                :options="['', 'train']"
                @change="updateDf()"
                class="mt-2"
              />
            </b-col>
            <b-col>
              🌎 Category<br>
              <b-form-select
                v-model="category"
                :options="categories"
                @change="updateDf()"
                class="mt-2"
              />
            </b-col>
            <b-col>
              🎯 Tag<br>
              <b-form-select
                v-model="tag"
                :options="tags"
                @change="updateDf()"
                class="mt-2"
              />
            </b-col>
            <b-col>
              📖 Page<br>
              <b-form-spinbutton
                id="top_page_select"
                v-model="page"
                min="1"
                max="100000"
                inline
                @change="updateDf()"
                class="mt-2"
              />
            </b-col>
          </b-row>
        </b-container>
      </font>
    </b-card>
    <b-container fluid>
      <b-row>
        <b-col v-for="(el, key, n) in df" :key="key">
          <b-card no-body class="mt-2 mx-n2"
            border-variant="primary"
          >
          <div>
            【{{ n+(page-1)*contentsIn1Page+1 }}.】
            {{ el.like.toFixed(3) }}
          </div>
            <a :href="el.url" target="_blank">
              <b-img-lazy
                :src="imagePath(el.id)"
                width="240"
                center
              />
            </a>
            <div>
              {{ el.item }}
              ({{ el.category }})
            </div>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
    <b-container
      class="d-flex justify-content-center my-2"
    >
      <b-form-spinbutton
        id="bottom_page_select"
        v-model="page"
        min="1"
        max="100000"
        inline
        @change="updateDf()"
      />
    </b-container>
    <b-container
      class="d-flex justify-content-center my-2"
    >
    <b-button
        variant="primary"
        @click="scrollTop"
      >scroll to top</b-button>
    </b-container>
  </div>
</template>

<script>
import axios from "axios"
import hostname from "raw-loader!../../setting/hostname.txt"
import port from "raw-loader!../../setting/port_flask.txt"

var endpoint = "http://" + hostname + ":" + port
var defaultPage = 1
var defaultContentsToShow = ""
var defaultContentsIn1Page = 7*14
var defaultCategory = ""
var defaultTag = ""

// function to get keys from sorted obj by values
function keysFromObj(fruits){
  var pairs = Object.entries(fruits);
  pairs.sort(function(p1, p2){
    var p1Val = p1[1], p2Val = p2[1];
    return p2Val - p1Val;
  })
  return pairs.map(item => item[0]);
}

export default {
  data() {
    return {
      page: defaultPage,
      contentsToShow: defaultContentsToShow,
      contentsIn1Page: defaultContentsIn1Page,
      category: defaultCategory,
      tag: defaultTag,
      categories: [],
      tags: [],
			df: [],
    }
  },
  methods:{
    imagePath(index) {
        return endpoint + "/image?id=" + parseInt(index)
    },
    updateDf() {
      var url = new URL(endpoint + "/datas")
      url.searchParams.append("page", this.page)
      url.searchParams.append("contentsToShow", this.contentsToShow)
      url.searchParams.append("contentsIn1Page", this.contentsIn1Page)
      url.searchParams.append("category", this.category)
      url.searchParams.append("tag", this.tag)
      axios
        .get(url)
        .then((response) => (this.df = response.data))
    },
    scrollTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      })
    }
  },
  mounted() {
    this.updateDf()
    axios
      .get(endpoint + "/categories")
      .then((response) => (this.categories = keysFromObj(response.data)))
      axios
      .get(endpoint + "/tags")
      .then((response) => (this.tags = response.data))
  }
}
</script>
