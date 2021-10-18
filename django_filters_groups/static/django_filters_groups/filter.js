function _createRemoveButton() {
  let removeButton = document.createElement("button");
  removeButton.className = "filter-remove-btn";
  removeButton.type = "button";
  return removeButton;
}

function _wrapElement(element, wrapperElement) {
  let wrapper = wrapperElement || document.createElement("div");
  element.parentNode.insertBefore(wrapper, element);
  wrapper.appendChild(element);
}

function _removeFilter(selectedFilters, filterName) {
  let filter = selectedFilters.querySelector(`[data-filter-name=${filterName}] .filter`);
  if (filter) {
    let filterGroup = filter.querySelector(".filter-group");
    filterGroup.querySelector("[name]").value = "";
    let filterBlock = filter.closest(".filter-block");
    filterBlock.append(filterGroup);
    filter.remove();
    filterGroup.classList.remove("filter-group");
    filterBlock.querySelectorAll(":disabled").forEach((el) => (el.disabled = false));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  let allFilters = document.getElementById("allFiltersByGroups");

  let selectToChooseFilter = document.getElementById("id_filter");
  let filterSelectInitialOptions = [...selectToChooseFilter.options];

  let selectedFilters = document.getElementById("selectedFilters");
  for (const element of selectedFilters.querySelectorAll(".filter-wrapper")) {
    let filterLookupBlock = element.querySelector(".filter-lookup");
    let filterName = filterLookupBlock.dataset.filterLookup;
    let selectedFilterNameArray = [filterName];
    let selectedLookup = filterLookupBlock.querySelector("select").selectedOptions[0].value;
    if (selectedLookup && selectedLookup !== "exact") {
      selectedFilterNameArray.push(selectedLookup);
    }
    let selectedFilterName = selectedFilterNameArray.join("__");

    // wrap applied filters with .filter and .filter-group classes
    let SelectedFilter = element.querySelector(`[name=${selectedFilterName}`);
    let elementToWrap = SelectedFilter.closest(filterDefaults.filterWrapperSelector);
    elementToWrap.classList.add("filter-group");

    let wrapper = document.createElement("div");
    wrapper.className = "filter";
    _wrapElement(elementToWrap, wrapper);
    wrapper.appendChild(_createRemoveButton());

    // disable unselected filters for current element
    element.querySelectorAll(`.filter-block [name^=${filterName}]`).forEach((el) => {
      if (el !== SelectedFilter) {
        el.disabled = true;
      }
    });

    // remove selected from available to choose filter
    let selectedOptionIndex = [...selectToChooseFilter.options].findIndex((el) => el.value === filterName);
    selectToChooseFilter.remove(selectedOptionIndex);
  }

  selectToChooseFilter.addEventListener("change", (e) => {
    let selectedValue = e.target.selectedOptions[0].value;
    selectToChooseFilter.remove(e.target.selectedIndex);

    let selectedElements = {
      lookup: document.querySelector(`[data-filter-lookup=${selectedValue}]`),
      filters: document.querySelector(`[data-filter-name=${selectedValue}]`).cloneNode(false),
      wrapper: document.querySelector(`[data-filter-lookup=${selectedValue}]`).closest(".filter-wrapper"),
    };
    selectedFilters.insertBefore(selectedElements.wrapper, selectedFilters.querySelector(".filter-button"));
    selectedElements.lookup.classList.add("filter-lookup--selected");
    selectedElements.filters.classList.add("filter-block--selected");
  });

  // select/change filter lookup
  document.querySelectorAll("[data-filter-lookup]").forEach((el) => {
    el.addEventListener("change", (e) => {
      let selectedValue = e.target.selectedOptions[0].value;
      let filterName = el.dataset.filterLookup;
      let filterWrapper = el.closest(".filter-wrapper");
      let blockToSelectFilter = filterWrapper.querySelector(`[data-filter-name=${filterName}]`);

      if (selectedValue) {
        if (selectedValue === "exact") {
          selectedValue = "";
        }
        _removeFilter(selectedFilters, filterName);
        let filterToSelect = blockToSelectFilter.querySelector(
          `[name=${[filterName, selectedValue].filter(Boolean).join("__")}]`
        );
        [...filterWrapper.querySelectorAll(`[name^=${filterName}]`)].forEach((el) => {
          if (el !== filterToSelect) {
            el.disabled = true;
          }
        });
        let rowWithRemoveButton = document.createElement("div");
        rowWithRemoveButton.className = "filter";

        let group = filterToSelect.closest(filterDefaults.filterWrapperSelector);
        group.classList.add("filter-group");
        _wrapElement(group, rowWithRemoveButton);
        rowWithRemoveButton.appendChild(_createRemoveButton());
      } else if (blockToSelectFilter) {
        _removeFilter(selectedFilters, filterName);
      }
    });
  });

  // remove filter button click
  selectedFilters.addEventListener("click", (e) => {
    let target = e.target;
    if (target.classList.contains("filter-remove-btn")) {
      let filterWrapper = target.closest(".filter-wrapper");
      let filterName = target.closest("[data-filter-name]").dataset.filterName;
      _removeFilter(selectedFilters, filterName);
      allFilters.appendChild(filterWrapper);
      let lookupGroup = filterWrapper.querySelector(".filter-lookup--selected");
      lookupGroup.classList.remove("filter-lookup--selected");
      lookupGroup.querySelector("select").selectedIndex = 0;

      selectToChooseFilter.add(filterSelectInitialOptions.filter((el) => el.value === filterName)[0]);
      selectToChooseFilter.selectedIndex = 0;

      if (filterDefaults.submitOnFilterDelete) {
        document.getElementById("submitFilters").click();
      }
    }
  });

  document.getElementById("clearFilters").addEventListener("click", () => {
    let data = new FormData();
    document
      .getElementById("filters")
      .querySelectorAll("form [name]")
      .forEach((el) => data.append(el.getAttribute("name"), el.value));
    let params = new URLSearchParams(location.search);
    for (let key of data.keys()) {
      params.delete(key);
    }
    location.search = params.toString();
  });
});
