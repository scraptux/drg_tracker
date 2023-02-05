<template>
  <div>
    <LoadingAnimation v-if="!svg.loaded"></LoadingAnimation>
    <div v-if="svg.loaded" id="timeline-container">
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import LoadingAnimation from '@/components/LoadingAnimation.vue'

export default {
  name: 'TrackingSVG',
  props: ['drg', 'code', 'year', 'years'],
  /*props: {
    drg: {type: String},
    code: {type: String},
    year: {type: String},
    years: {
      type: Object,
      required: true
    }
  },*/
  watch: {
    years: {
      handler: function(newYears, oldYears) {
        //console.log("called")
        //console.log(this.years)
        if (this.svg.loaded) {
          //console.log("calling")
          this.createTimeline(newYears[0], newYears[1])
          this.svg.loaded = false
          console.log(newYears[0], newYears[1])
          this.loadSVGData(newYears[0], newYears[1])
        }
      },
      deep: true
    }
  },
  data() {
    return {
      svg: {
        'loaded': false
      }
    }
  },
  async created() {
    this.loadSVGData(this.years[0], this.years[1])
    //this.createTimeline(0, 30);
  },
  methods: {
    async loadSVGData(start_year, stop_year) {
      try {
        //await axios.get(`${this.$baseURL}/api/${this.drg}/track/?year=${this.year}&code=${this.code}`).then(async res => {
        await axios.get(`${this.$baseURL}/api/${this.drg}/track/?code=${this.code}&year_start=${start_year}&year_stop=${stop_year}&year=${this.year}`).then(async res => {
          this.svg.years = res.data.years
          this.svg.nodes = res.data.nodes
          this.svg.links = res.data.links
          this.svg.code_count = res.data.code_count
          this.svg.loaded = true

          //console.log(this.svg.years[this.svg.years.length-1].text)
          //this.createTimeline(this.years[0], this.years[1])
        })
      } catch(e) {
        console.log(e)
      }
      this.createTimeline(this.svg.years[0].text, this.svg.years[this.svg.years.length-1].text)
    },
    createTimeline(start_year, stop_year) { // start_year and stop_year take indices
      //console.log("drawing")
      var getCoords = this.getCoords
      var data = this.svg
      //console.log(data)
      start_year = parseInt(start_year)-parseInt(data.years[0].text)
      stop_year = parseInt(stop_year)-parseInt(data.years[0].text)

      var years_adj = [];
      data.years.forEach((year) => {
        if (start_year <= year.y && year.y <= stop_year) {
          years_adj.push({'y': year.y-start_year, 'text': year.text});
        }
      });
      var links_adj = [];
      data.links.forEach((link) => {
        var link_tmp = {'source': {}, 'target': {}};
        if (start_year <= link.source.y && start_year <= link.target.y && link.source.y <= stop_year && link.target.y <= stop_year) { // reorder coords
          link_tmp.source.x = link.source.x;
          link_tmp.source.y = link.source.y - start_year;
          link_tmp.target.x = link.target.x;
          link_tmp.target.y = link.target.y - start_year;
        } else { // remove unwanted links
          return;
        }
        links_adj.push(link_tmp);
      });
      var nodes_adj = [];
      data.nodes.forEach((node) => {
        if (start_year <= node.y && node.y <= stop_year) {
          nodes_adj.push({'x': node.x, 'y': node.y - start_year, 'text': node.text})
        }
      });

      data.height = (data.code_count*100+50)-60;
      data.width = years_adj.length*100-40;

      d3.select("#timeline-container").selectAll("*").remove();
      var svg = d3.select("#timeline-container")
        .append("svg")
        .attr("viewBox", "0 0 "+data.width+" "+data.height)
        //.attr("width", data.width)
        //.attr("height", data.height)
        .style("max-height", (data.height*0.8)+"px")
        .attr("class", "mx-auto")
        .append("g");
        
      //svg.append('line').style('stroke', 'blue').attr('x1', 0).attr('y1', data.height).attr('x2', data.width).attr('y2', 0);

      var year = svg.selectAll(".year")
        .data(years_adj)
        .enter().append("text")
        .attr("x", function(d) { return getCoords(d, "x"); })
        .attr("y", function(d) { return getCoords({'y': d.y, 'x': data.code_count-1}, "y"); }).attr("dy", 50)
        .attr("font-weight", 500).attr("font-size", 20)
        .style("text-anchor", "middle")
        .text(function(d) { return d.text; });

      var diagonal = d3.svg.diagonal()
        .source(function(d) { return getCoords(d.source, "source"); })
        .target(function(d) { return getCoords(d.target, "target"); })
        .projection(function(d) { return [d.y, d.x]; });
   
      var fork = svg.selectAll(".link")
        .data(links_adj)
        .enter().append("path")
        .attr("class", "link")
        .attr("d", diagonal);
   
      var circle = svg.selectAll(".circle")
        .data(nodes_adj)
        .enter()
        .append("g")
        .attr("class", "circle");
   
      var el = circle.append("circle")
        .attr("cx", function(d) { return getCoords(d, "x"); })
        .attr("cy", function(d) { return getCoords(d, "y"); })
        .attr("r", 10)
        .style("fill", "blue");

      var text = circle.append("text")
        .attr("x", function(d) { return getCoords(d, "x"); })
        .attr("y", function(d) { return getCoords(d, "y"); })
        .attr("dx", 0).attr("dy", -15)
        .attr("font-weight", 300)
        .style("text-anchor", "middle")
        .text(function(d) { return d.text; });
    },
    getCoords(d, ret="") {
      if (ret == "source") { // x,y für Links
        var x = d.x*100+30;
        var y = d.y*100+30;
        return {"x": x, "y": y};
      } else if (ret == "target") {
        x = d.x*100+30;
        y = d.y*100+30;
        return {"x": x, "y": y};
      } else if (ret == "x") { // x für Nodes/Text
        return d.y*100+30;
      } else if (ret == "y") { // y für Nodes/Text
        return d.x*100+30;
      }
    }
  },
  components: { LoadingAnimation }
}
</script>