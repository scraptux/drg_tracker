import axios from "axios";

class Tracker {
    constructor(ystart, ystop, load = true) {
        this.loading = true;
        this.clearData(ystart, ystop);
        if (load) {
            this.load();
        }
        //this.loading = false;
    }

    async addCode(drg, code) {
        for (let v in this.vars) {
            if (this.vars[v].name != this.displayedVar) {
                continue;
            }
            await this.vars[v].addCode(drg, code, this.ystart, this.ystop);
            break;
        }
        this.save();
    }

    addVar(name) {
        let v = new Variable(name);
        this.vars.push(v);
        this.setDisplayedVar(name);
        this.sort();
        this.save();
    }

    changeVarName(newname) {
        // return if newname is already taken
        for (let v in this.vars) {
            if (v.name == newname) {
                return;
            }
        }
        let oldname = this.displayedVar;

        for (let v in this.vars) {
            if (this.vars[v].name != oldname) {
                continue;
            }
            this.vars[v].name = newname;
            break;
        }

        this.displayedVar = newname;
        this.sort();
        this.save();
    }

    clearData(ystart, ystop) {
        this.vars = [new Variable("Neue Variable")];
        this.ystart = ystart;
        this.ystop = ystop;
        this.ysearch = ystop;
        this.displayedVar = "Neue Variable";
        let range = document.getElementById('timelineslider');
        if (!range.noUiSlider) {
            return;
        }
        range.noUiSlider.set([this.ystart, this.ystop]);
    }

    containsVar(name) {
        return this.vars.filter((v) => v.name == name).length >= 1;
    }

    delCode(code) {
        this.getDisplayedVar().delCode(code);
        this.save();
    }

    delVar(name) {
        if (this.vars.length <= 1) {
            this.clearData();
        } else {
            this.vars = this.vars.filter((v) => v.name != name);
        }
        if (!this.containsVar(this.displayedVar)) {
            this.displayedVar = this.vars[0].name;
        }
        this.save();
    }

    fetchMissing() {
        this.vars.map((e) => e.fetchMissing(this.ystart, this.ystop));
    }

    fromJson(json) {
        this.vars = json.vars.map((e) => Variable.fromJson(e, json.ystart, json.ystop));
        this.ystart = json.ystart;
        this.ystop = json.ystop;
        if (json.ysearch) {
            this.ysearch = json.ysearch;
        }
        this.displayedVar = json.displayedVar;
    }

    getDisplayedVar() {
        return this.vars.filter((v) => v.name == this.displayedVar)[0];
    }

    load() {
        let storedString = localStorage.getItem('tracker');
        if (storedString) {
            this.fromJson(JSON.parse(storedString));
        }
        this.loading = false;
    }

    async refetchData() {
        for (let v in this.vars) {
            this.vars[v].clearData();
        }
        this.save();
        for (let v in this.vars) {
            if (this.vars[v].name == this.displayedVar) {
                await this.vars[v].refetchData(this.ystart, this.ystop);
                break;
            }
        }
    }

    save() {
        localStorage.tracker = JSON.stringify(this);
    }

    saveEditData(code) {
        this.getDisplayedVar().saveEditData(code);
        this.save();
    }

    setAvailableYears(ystart, ystop) {
        if (this.ystart && this.ystop) {
            return;
        }
        this.ystart = ystart;
        this.ystop = ystop;
        if (this.ystart > this.ysearch || this.ystop < this.ysearch) {
            this.ysearch = this.ystop;
        }
    }

    setDisplayedVar(name) {
        this.displayedVar = name;
        this.vars.filter((v) => v.name == name)
            .map((v) => v.setDisplayed(this.ystart, this.ystop));
    }

    setYears(ystart, ystop) {
        if (this.ystart == ystart && this.ystop == ystop) {
            return;
        }
        this.ystart = ystart;
        this.ystop = ystop;
        if (this.ystart > this.ysearch || this.ystop < this.ysearch) {
            this.ysearch = this.ystop;
        }
        this.refetchData();
        // this.save();  // TODO: currently has no effect
    }

    sort() {
        this.vars = this.vars.sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    }
}

class Variable {
    constructor(name) {
        this.name = name;
        this.codes = [];
    }

    static fromJson(json, ystart, ystop) {
        let v = new Variable(json.name);
        v.codes = json.codes.map((e) => Code.fromJson(e, ystart, ystop));
        return v;
    }

    async addCode(drg, code, ystart, ystop) {
        let c = new Code(drg, code);
        //await c.fetchData(ystart, ystop);
        this.codes.push(c);
        /*this.codes.filter((e) => e.code == code)
            .map((e) => e.fetchData(ystart, ystop));*/
        for (let i in this.codes) {
            if (this.codes[i].code != code) {
                continue;
            }
            await this.codes[i].fetchData(ystart, ystop);
        }
        this.sort();
    }

    clearData() {
        this.codes.map((c) => c.clearData());
    }

    containsCode(code) {
        return this.codes.filter((c) => c.code == code).length >= 1;
    }

    delCode(code) {
        this.codes = this.codes.filter((c) => c.code != code);
    }

    fetchMissing(ystart, ystop) {
        this.codes.map((e) => e.fetchMissing(ystart, ystop));
    }

    getCode(code) {
        return this.codes.filter((c) => c.code == code)[0];
    }

    loaded() {
        return this.codes.find((c) => c.loaded()).length >= 1;
    }

    async refetchData(ystart, ystop) {
        // TODO improve
        this.codes.map(async (c) => await c.refetchData(ystart, ystop));
        this.loaded = true;
    }

    saveEditData(code) {
        this.getCode(code).saveEditData();
    }

    setDisplayed(ystart, ystop) {
        this.codes.filter((c) => (c.data == null && !c.loading))
            .map((c) => c.fetchData(ystart, ystop));
    }

    sort() {
        this.codes = this.codes.sort((a, b) => a.code.toLowerCase().localeCompare(b.code.toLowerCase()));
    }
}

class Code {
    constructor(drg, code) {
        this.drg = drg;
        this.code = code;
        this.loading = false;
        this.error = "";
        this.data = null;
    }

    static fromJson(json, ystart, ystop) {
        let c = new Code(json.drg, json.code);
        c.error = json.error;
        c.loading = json.loading;
        if (json.data) {
            c.data = CodeData.fromJson(json.data);
        }
        return c;
    }

    clearData() {
        this.loading = false;
        this.error = "";
        this.data = null;
    }

    async fetchData(ystart, ystop) {
        try {
            this.loading = true;
            await axios.get(`/api/${this.drg}/track/?code=${this.code}&year_start=${ystart}&year_stop=${ystop}`).then(res => {
                // TODO: check for data validity
                this.data = new CodeData(res.data);
                this.data.checkCodeData(this.code, ystart, ystop);
                this.error = "";
                this.loading = false;
            });
        } catch (e) {
            this.error = "Code konnte nicht geladen werden";
            this.loading = false;
            console.log(e);
        }
    }

    async fetchMissing(ystart, ystop) {
        if (!this.data || this.loading) {
            await this.fetchData(ystart, ystop);
        }
    }

    loaded() {
        return !(this.loading || this.data == {});
    }

    async refetchData(ystart, ystop) {
        this.clearData();
        await this.fetchData(ystart, ystop);
    }

    saveEditData() {
        if (this.data.edit_status == 0) {
            this.data.edit_status = 1;
        } else if (this.data.edit_status == 2) {
            this.data.edit_status = 3;
        }
    }
}

class CodeData {
    constructor(data) {
        this.code_data = data;
        this.edit_status = 0;
        this.edit_data = [];
    }

    static fromJson(json) {
        let cd = new CodeData(json.code_data);
        cd.edit_status = json.edit_status;
        cd.edit_data = json.edit_data.map((cdf) => CodeDataField.fromJson(cdf));
        return cd;
    }

    checkCodeData(code, ystart, ystop) {
        let selected_found = false;
        // check all subcodes for given codes
        for (let c of this.code_data.code_list) {
            // check if subcode is user-selected code
            let selected = false;
            if (code == c.replace('.', '').replace('-', '')) {
                selected = true;
                selected_found = true;
            }
            // add selectable code for each year
            for (let year = ystart; year <= ystop; year++) {
                let cdf = new CodeDataField(c, year, selected ? true : false);
                this.edit_data.push(cdf);
            }
        }
        // manually add selected code if not in subcodes
        if (!selected_found) {
            for (let year = ystart; year <= ystop; year++) {
                let cdf = new CodeDataField(code, year, true);
                this.edit_data.push(cdf);
            }
        }

        this.sort();
    }

    byCode() {
        return this.uniqueCodes().map((c) => this.getCode(c));
    }

    getCode(code) {
        return this.edit_data.filter((c) => c.code == code)
    }

    resetEditData() {
        let code = this.code_data.code.Code.replace('.', '').replace('-', '');
        let ystart = this.uniqueYears()[0];
        let ystop = this.uniqueYears()[this.uniqueYears().length - 1];
        this.edit_data = [];
        this.checkCodeData(code, ystart, ystop);
    }

    sort() {
        this.edit_data = this.edit_data.sort((a, b) => a.year > b.year)
            .sort((a, b) => a.code.toLowerCase().localeCompare(b.code.toLowerCase()));
    }

    uniqueCodes() {
        return [...new Set(this.edit_data.map((c) => c.code))];
    }

    uniqueYears() {
        if (!this.edit_data) {
            return;
        }
        return [...new Set(this.edit_data.map((c) => c.year))];
    }
}

class CodeDataField {
    constructor(code, year, selected) {
        this.code = code;
        this.year = year;
        this.selected = selected;
    }

    static fromJson(json) {
        let cdf = new CodeDataField(json.code, json.year, json.selected);
        return cdf;
    }

    toggleSelected() {
        this.selected = !this.selected;
    }
}


export { Tracker };