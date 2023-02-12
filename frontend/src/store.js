import { reactive } from 'vue'
import axios from 'axios'

export const store = reactive({
  available_years: [],

  search_year: 0,
  displayed_var: "",
  tracking_years: [],
  tracking_vars: {},
  show_info: "",
  show_prompt: "",
  share_code: "",
  notifications: [],
  /* LOAD AND SAVE */
  loadFromFileCSV(store, file) {
    // var;code;drg;added_year;year;edit_code;edit_data
    let data = file.target.result.split("\r\n")
    let used_years = []
    for (let line = 0; line < data.length; line++) {
      if (data[line] == "") {
        continue
      }
      let cells = data[line].split(";")
      if (cells[4] in used_years) {
        break
      }
      used_years.push(cells[4])
    }
    store.tracking_years[0] = Math.min.apply(Math, used_years)
    store.tracking_years[1] = Math.max.apply(Math, used_years)
    store.updateYearSlider()
    store.tracking_vars = {}
    for (let line = 0; line < data.length; line++) {
      if (data[line] == "") {
        continue
      }
      let cells = data[line].split(";")
      if (!(cells[0] in store.tracking_vars)) {
        store.tracking_vars[cells[0]] = {}
      }
      if (!(cells[1] in store.tracking_vars[cells[0]])) {
        store.tracking_vars[cells[0]][cells[1]] = {}
        store.tracking_vars[cells[0]][cells[1]].drg = cells[2]
        store.tracking_vars[cells[0]][cells[1]].year = cells[3]
        store.tracking_vars[cells[0]][cells[1]].edit_code = cells[5]
        store.tracking_vars[cells[0]][cells[1]].edit_data_imported = {}
        store.tracking_vars[cells[0]][cells[1]].loading = true
      }
      if (cells[5] >= 2) {
        let codes = cells[6].split(",")
        store.tracking_vars[cells[0]][cells[1]].edit_data_imported[cells[4]] = codes
      }
    }
    for (var key in this.tracking_vars) {
      if (key != "") {
        store.setDisplayedVar(key)
        break
      }
    }
    store.sendNotification("Datei geladen.")
    store.saveToStorage()
  },
  loadFromFileJSON(store, file) {
    let data = JSON.parse(file.target.result)
    store.tracking_years = data.tracking_years
    store.updateYearSlider()
    store.tracking_vars = data.tracking_vars
    for (let variable in store.tracking_vars) {
      for (let code in store.tracking_vars[variable]) {
        store.tracking_vars[variable][code].loadedFromFile = true
      }
    }
    store.setDisplayedVar(data.displayed_var)
    store.sendNotification("Datei geladen.")
    store.saveToStorage()
  },
  loadFromStorage() {
    let tracking_years = localStorage.getItem("tracking_years")
    let tracking_vars = localStorage.getItem("tracking_vars")
    let tracking_displayed_var = localStorage.getItem("tracking_displayed_var")
    if (tracking_years === null && tracking_vars === null && tracking_displayed_var === null) {
      throw new Error("No Data")
    }
    this.tracking_years = JSON.parse(tracking_years)
    this.search_year = this.tracking_years[1]
    this.tracking_vars = JSON.parse(tracking_vars)
    this.setDisplayedVar(tracking_displayed_var)
  },
  saveToStorage() {
    localStorage.tracking_years = JSON.stringify(this.tracking_years)
    localStorage.tracking_vars = JSON.stringify(this.tracking_vars)
    localStorage.tracking_displayed_var = this.displayed_var
  },
  saveToFile(format) {
    let data = null
    let blob = null
    if (format == 'json') {
      data = this.saveToFileJSON()
      blob = new Blob([JSON.stringify(data)], {type: "application/json;charset=utf-8"})
    } else if (format == 'csv') {
      data = this.saveToFileCSV()
      blob = new Blob([data], {type: "text/csv;charset=utf-8"})
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
  saveToFileCSV() {
    // var;code;drg;added_year;year;edit_code;edit_data
    let data = []
    for (let variable in this.tracking_vars) {
      for (let code in this.tracking_vars[variable]) {
        for (let year = this.tracking_years[0]; year <= this.tracking_years[1]; year++) {
          if (this.tracking_vars[variable][code].loading || this.tracking_vars[variable][code].edit_code == 0) {
            data.push([variable, code, this.tracking_vars[variable][code].drg, this.tracking_vars[variable][code].year, year, 0, ""])
          } else if (this.tracking_vars[variable][code].edit_code == 1) {
            data.push([variable, code, this.tracking_vars[variable][code].drg, this.tracking_vars[variable][code].year, year, 1, ""])
          } else {
            let edit_data = []
            for (let edit_item in this.tracking_vars[variable][code].edit_data) {
              if (this.tracking_vars[variable][code].edit_data[edit_item][year].checked) {
                edit_data.push(edit_item)
              }
            }
            data.push([variable, code, this.tracking_vars[variable][code].drg, this.tracking_vars[variable][code].year, year, this.tracking_vars[variable][code].edit_code, edit_data.join(",")])
          }
        }
      }
    }
    let data_string = ""
    data.forEach(function(row) {
      data_string += row.join(";")+"\r\n"
    })
    return data_string
  },
  saveToFileJSON() {
    let data = {}
    data.tracking_years = this.tracking_years
    data.tracking_vars = {}
    data.displayed_var = this.displayed_var
    for (let variable in this.tracking_vars) {
      data.tracking_vars[variable] = {}
      for (let code in this.tracking_vars[variable]) {
        data.tracking_vars[variable][code] = {}
        data.tracking_vars[variable][code].drg = this.tracking_vars[variable][code].drg
        data.tracking_vars[variable][code].edit_code = this.tracking_vars[variable][code].edit_code
        data.tracking_vars[variable][code].edit_data = this.tracking_vars[variable][code].edit_data
        data.tracking_vars[variable][code].year = this.tracking_vars[variable][code].year
      }
    }
    return data
  },
  /* SETTER */
  addCode(drg, code) {
    this.tracking_vars[this.displayed_var][code] = {'drg': drg, 'year': this.search_year}
    this.tracking_vars[this.displayed_var] = this.sortObject(this.tracking_vars[this.displayed_var])
    this.loadTrackingInfo(this.displayed_var, code)
    this.saveToStorage()
  },
  addVariable(varname) {
    this.tracking_vars[varname] = {}
    this.tracking_vars = this.sortObject(this.tracking_vars)
    this.setDisplayedVar(varname)
    this.saveToStorage()
  },
  changeVariableName(newname) {
    let oldname = this.displayed_var
    this.addVariable(newname)
    this.tracking_vars[newname] = this.tracking_vars[oldname]
    this.deleteVariable(oldname)
    this.saveToStorage()
  },
  deleteCode(code) {
    delete this.tracking_vars[this.displayed_var][code]
    this.saveToStorage()
  },
  deleteData() {
    this.tracking_vars = {}
    this.tracking_vars["Neue Variable"] = {}
    this.setDisplayedVar("Neue Variable")
    this.setTrackingYears([this.available_years[0].Year, this.available_years[this.available_years.length-1].Year])
    this.setSearchYear(this.available_years[this.available_years.length-1].Year)
    this.sendNotification("Alle Daten gelöscht.")
    this.saveToStorage()
  },
  deleteNotification(index) {
    this.notifications.splice(index, 1)
    this.notifications.unshift("")
  },
  deleteVariable(varname) {
    let newname = ""
    for (var key in this.tracking_vars) {
      if (key != varname) {
        newname = key
        break
      }
    }
    delete this.tracking_vars[varname]
    if (newname == "") {
      this.addVariable("Neue Variable")
      return
    }
    this.setDisplayedVar(newname)
    this.saveToStorage()
  },
  async sendNotification(s) {
    this.notifications.push(s)
    await new Promise(resolve => setTimeout(resolve, 3000))
    this.notifications.shift()
  },
  setDisplayedVar(varname) {
    this.displayed_var = varname
    for (var code in this.tracking_vars[varname]) {
      if (!('loading' in this.tracking_vars[varname][code]) || this.tracking_vars[varname][code].loading) {
        this.loadTrackingInfo(varname, code)
      }
    }
  },
  setSearchYear(year) {
    this.search_year = year
  },
  setTrackingYears(years) {
    if (years[0] == this.tracking_years[0] && years[1] == this.tracking_years[1]) {
      return
    }
    if (this.tracking_years.length == 0) {
      this.tracking_years = years
      return
    } else {
      this.tracking_years = years
    }
    // reload all codes
    for (var variable in this.tracking_vars) {
      for (var code in this.tracking_vars[variable]) {
        delete this.tracking_vars[variable][code].data
        delete this.tracking_vars[variable][code].edit_code
        delete this.tracking_vars[variable][code].edit_data
        this.loadTrackingInfo(variable, code)
      }
    }
    // set searchyear
    if (this.search_year > years[1]) {
      this.search_year = years[1]
    } else if (this.search_year < years[0]) {
      this.search_year = years[0]
    }
    this.saveToStorage()
  },
  updateYearSlider() {
    let range = document.getElementById('timelineslider')
    range.noUiSlider.updateOptions({
      start: this.tracking_years
    })
  },
  /* API CALLS */
  async loadTrackingInfo(variable, code) {
    this.tracking_vars[variable][code].loading = true
    if (variable != this.displayed_var) {
      return
    }
    try {
      await axios.get(`/api/${this.tracking_vars[variable][code].drg}/track/?code=${code}&year_start=${this.tracking_years[0]}&year_stop=${this.tracking_years[1]}&year=${this.tracking_vars[variable][code].year}`).then(res => {
        this.tracking_vars[variable][code].data = res.data
        if ('edit_code' in this.tracking_vars[variable][code]) {
          if ('edit_data_imported' in this.tracking_vars[variable][code]) {
            this.reformatEditData(variable, code)
          }
        } else {
          this.resetEditData(variable, code)
        }
        this.tracking_vars[variable][code].loading = false
      })
    } catch (e) {
      console.log(e)
    }
  },
  reformatEditData(variable, editcode) {
    let code = this.tracking_vars[variable][editcode].edit_code
    if (code <= 1) {
      this.resetEditData(variable, editcode)
      this.tracking_vars[variable][editcode].edit_code = code
      delete this.tracking_vars[variable][editcode].edit_data_imported
    } else {
      this.resetEditData(variable, editcode)
      this.tracking_vars[variable][editcode].edit_code = code
      for (let code in this.tracking_vars[variable][editcode].edit_data) {
        for (let year = this.tracking_years[0]; year <= this.tracking_years[1]; year++) {
          if (this.tracking_vars[variable][editcode].edit_data_imported[year].indexOf(code) > -1) {
            this.tracking_vars[variable][editcode].edit_data[code][year].checked = true
          } else {
            this.tracking_vars[variable][editcode].edit_data[code][year].checked = false
          }
        }
      }
      delete this.tracking_vars[variable][editcode].edit_data_imported
    }
  },
  resetEditData(variable, editcode) {
    this.tracking_vars[variable][editcode].edit_code = 0
    this.tracking_vars[variable][editcode].edit_data = {}
    let editcode_found = false
    for (let code of this.tracking_vars[variable][editcode].data.code_list) {
      if (!(code in this.tracking_vars[variable][editcode].edit_data)) {
        this.tracking_vars[variable][editcode].edit_data[code] = {}
      }
      let field_data = {'Code': code, 'checked': false}
      if (editcode == code.replace('.','').replace('-','')) {
        field_data.checked = true
        editcode_found = true
      }
      for (let year = this.tracking_years[0]; year <= this.tracking_years[1]; year++) {
        this.tracking_vars[variable][editcode].edit_data[code][year] = {...field_data}
      }
    }
    if (!editcode_found) {
      this.tracking_vars[variable][editcode].edit_data[editcode] = {}
      for (let year = this.tracking_years[0]; year <= this.tracking_years[1]; year++) {
        this.tracking_vars[variable][editcode].edit_data[editcode][year] = {'Code': editcode, 'checked': true}
      }
    }
    this.tracking_vars[variable][editcode].edit_data = this.sortObject(this.tracking_vars[this.displayed_var][editcode].edit_data)
  },
  /* HELPER */
  sortObject(o) {
    let unsorted = o
    o = Object.keys(unsorted).sort(function(a, b) {
      return a.toLowerCase().localeCompare(b.toLowerCase())
    }).reduce(function(v, i) {
      v[i] = unsorted[i]
      return v
    }, {})
    return o
  }
})