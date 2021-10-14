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

function _removeFromSelect(select, index) {
  select.remove(index);
  if (select.options.length === 1) {
    select.removeAttribute("required");
  }
}

function _removeFilter(selectedFilters, filterLookup) {
  let filter = selectedFilters.querySelector(`[data-filter-name=${filterLookup}] .filter`);
  if (filter) {
    let filterGroup = filter.querySelector(".filter-group");
    let filterBlock = filter.closest(".filter-block");
    filterBlock.append(filterGroup);
    filter.remove();
    filterGroup.classList.remove("filter-group");
    filterBlock.querySelectorAll(":disabled").forEach((el) => el.removeAttribute("disabled"));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  let allFilters = document.getElementById("allFiltersByGroups");

  let filterSelect = document.getElementById("id_filter");
  let filterSelectInitialOptions = [...filterSelect.options];

  let selectedFilters = document.getElementById("selectedFilters");
  for (const element of selectedFilters.querySelectorAll(".filter-block")) {
    let filterName = element.dataset.filterName;
    let filter = element.querySelector(`[name^=${filterName}`);
    let elementToWrap = filter.closest(filterDefaults.filterWrapperSelector);
    elementToWrap.classList.add("filter-group");

    let wrapper = document.createElement("div");
    wrapper.className = "filter";
    _wrapElement(elementToWrap, wrapper);
    wrapper.appendChild(_createRemoveButton());

    // remove selected from available to choose filter
    let selectedOptionIndex = [...filterSelect.options].findIndex((el) => el.value === filterName);
    _removeFromSelect(filterSelect, selectedOptionIndex);

    // Select lookup in applied filters
    let lookupSelect = selectedFilters.querySelector(`[data-filter-lookup=${filterName}] select`);
    let selectedLookupArray = filter.getAttribute("name").split("__");
    let lookupToFind = selectedLookupArray[selectedLookupArray.length - 1];
    if (selectedLookupArray.length === 1) {
      lookupToFind = "exact";
    }
    lookupSelect.selectedIndex = [...lookupSelect.options].findIndex((el) => el.value === lookupToFind);
  }

  filterSelect.addEventListener("change", (e) => {
    let selectedValue = e.target.selectedOptions[0].value;
    _removeFromSelect(filterSelect, e.target.selectedIndex);

    let selectedElements = {
      lookup: document.querySelector(`[data-filter-lookup=${selectedValue}]`),
      filters: document.querySelector(`[data-filter-name=${selectedValue}]`).cloneNode(false),
      wrapper: document.querySelector(`[data-filter-lookup=${selectedValue}]`).closest(".filter-wrapper"),
    };
    selectedFilters.appendChild(selectedElements.wrapper);
    selectedElements.lookup.classList.add("filter-lookup--selected");
    selectedElements.filters.classList.add("filter-block--selected");
  });

  document.querySelectorAll("[data-filter-lookup]").forEach((el) => {
    el.addEventListener("change", (e) => {
      let selectedValue = e.target.selectedOptions[0].value;
      let filterLookup = el.dataset.filterLookup;
      let blockToSelectFilter = selectedFilters.querySelector(`[data-filter-name=${filterLookup}]`);

      if (selectedValue) {
        if (selectedValue === "exact") {
          selectedValue = "";
        }
        _removeFilter(selectedFilters, filterLookup);
        let filterToSelect = blockToSelectFilter.querySelector(
          `[name=${[filterLookup, selectedValue].filter(Boolean).join("__")}]`
        );
        [...blockToSelectFilter.querySelectorAll(`[name^=${filterLookup}]`)].map(
          (el) => el !== filterToSelect && el.setAttribute("disabled", "")
        );
        let rowWithRemoveButton = document.createElement("div");
        rowWithRemoveButton.className = "filter";

        let group = filterToSelect.closest(filterDefaults.filterWrapperSelector);
        group.classList.add("filter-group");
        _wrapElement(group, rowWithRemoveButton);
        rowWithRemoveButton.appendChild(_createRemoveButton());
      } else if (blockToSelectFilter) {
        _removeFilter(selectedFilters, filterLookup);
      }
    });
  });

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

      filterSelect.add(filterSelectInitialOptions.filter((el) => el.value === filterName)[0]);
      filterSelect.selectedIndex = 0;
    }
  });
});
