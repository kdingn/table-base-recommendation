<template>
  <div>
    <b-container
      class="d-flex justify-content-center mt-2"
    >
      <b-form-spinbutton
        id="top_page_select"
        v-model="page"
        min="1"
        max="100000"
        inline
        @change="updateDf()"
      />
    </b-container>
    <b-container fluid>
      <b-row>
        <b-col v-for="(el, key, n) in df" :key="key">
          <b-card no-body class="mt-2 mx-n2"
            border-variant="primary"
          >
          <div>
            【{{ n+(page-1)+contentsIn1Page }}.】
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
              ({{ el.author }})
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
  </div>
</template>

<script>
import axios from "axios";

var defaultPage = 1
var defaultContentsToShow = ""
var defaultContentsIn1Page = 7*14

export default {
  data() {
    return {
      page: defaultPage,
      contentsToShow: defaultContentsToShow,
      contentsIn1Page: defaultContentsIn1Page,
			df: [],
    }
  },
  methods:{
    imagePath(index) {
        return "http://localhost:5000/image?id=" + parseInt(index)
    },
    updateDf() {
      var url = new URL("http://localhost:5000/datas")
      url.searchParams.append("page", this.page)
      url.searchParams.append("contentsToShow", this.contentsToShow)
      url.searchParams.append("contentsIn1Page", this.contentsIn1Page)
      axios
        .get(url)
        .then((response) => (this.df = response.data))
    }
  },
  mounted() {
    this.updateDf()
    // var url = new URL("http://localhost:5000/datas")
    // url.searchParams.append("page", this.page)
    // url.searchParams.append("contentsToShow", this.contentsToShow)
    // url.searchParams.append("contentsIn1Page", this.contentsIn1Page)
    // axios
    //   .get(url)
    //   .then((response) => (this.df = response.data))
  },
}
</script>
