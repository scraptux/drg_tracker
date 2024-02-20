import { reactive } from 'vue'
import axios from 'axios'
import { Tracker } from './structs';

export const store = reactive({
  available_years: [],
  notifications: [],
  share_code: "",
  show_info: "",
  show_prompt: "",
  tracker: null,

  deleteNotification(idx) {
    this.notifications.splice(idx, 1);
    this.notifications.unshift("");
  },

  async getAvailableYears() {
    try {
      await axios.get(`/api/icd/version`).then(res => {
        // TODO: check validity
        this.available_years = res.data;
        if (this.tracker == null) {
          this.tracker = new Tracker(this.available_years[0], this.available_years[this.available_years.length-1]);
          this.tracker.setAvailableYears(this.available_years[0], this.available_years[this.available_years.length-1]);
          this.tracker.fetchMissing();
        } else {
          this.tracker.setAvailableYears(this.available_years[0], this.available_years[this.available_years.length-1]);
        }
      });
    } catch (e) {
      console.log(e);
    }
  },

  loadFromJson(str) {
    let o = JSON.parse(str);
    this.tracker = new Tracker(o.ystart, o.ystop, false);
    this.tracker.fromJson(o);
    this.tracker.loading = false;
    this.sendNotification("Daten wurden geladen.");
  },

  saveToFile(format) {
    let data = null
    let blob = null
    if (format == 'json') {
      data = this.saveToJson()
      blob = new Blob([data], {type: "application/json;charset=utf-8"})
    } else {
      return
    }
    const url = URL.createObjectURL(blob)
    const elem = document.createElement("a")
    elem.setAttribute('href', url)
    elem.setAttribute('download', 'code_tracking.'+format)
    document.body.appendChild(elem)
    elem.click()
    document.body.removeChild(elem)
  },

  saveToJson() {
    return JSON.stringify(this.tracker);
  },

  async sendNotification(s) {
    this.notifications.push(s)
    await new Promise(resolve => setTimeout(resolve, 3000))
    this.notifications.shift()
  },
});