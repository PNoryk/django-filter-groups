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
    };
    for (let el of Object.values(selectedElements)) {
      selectedFilters.appendChild(el);
    }
    selectedElements.lookup.classList.add("filter-lookup--selected");
    selectedElements.filters.classList.add("filter-block--selected");
  });

  document.querySelectorAll("[data-filter-lookup]").forEach((el) => {
    el.addEventListener("change", (e) => {
      let selectedValue = e.target.selectedOptions[0].value;
      let filterLookup = el.dataset.filterLookup;
      let blockToAddFilters = selectedFilters.querySelector(`[data-filter-name=${filterLookup}]`);
      let currentElementFilters = allFilters.querySelector(`[data-filter-name=${filterLookup}]`);

      if (selectedValue) {
        if (selectedValue === "exact") {
          selectedValue = "";
        }
        let filterToAdd = currentElementFilters.querySelector(
          `[name=${[filterLookup, selectedValue].filter(Boolean).join("__")}`
        );
        let rowWithRemoveButton = document.createElement("div");
        rowWithRemoveButton.className = "filter";

        let group = filterToAdd.closest(filterDefaults.filterWrapperSelector);
        group.classList.add("filter-group");

        rowWithRemoveButton.appendChild(group);
        rowWithRemoveButton.appendChild(_createRemoveButton());

        let oldFilter = selectedFilters.querySelector(`[data-filter-name=${filterLookup}] .filter`);
        if (oldFilter) {
          currentElementFilters.appendChild(oldFilter.querySelector(".filter-group"));
          oldFilter.remove();
        }

        blockToAddFilters.appendChild(rowWithRemoveButton);
      } else if (currentElementFilters) {
        let filter = selectedFilters.querySelector(`[data-filter-name=${filterLookup}] .filter`);
        currentElementFilters.appendChild(filter.querySelector(".filter-group"));
        filter.remove();
      }
    });
  });

  selectedFilters.addEventListener("click", (e) => {
    let target = e.target;
    if (target.classList.contains("filter-remove-btn")) {
      let filterBlock = target.closest("[data-filter-name]");
      let filterName = filterBlock.dataset.filterName;
      let filter = filterBlock.querySelector(`[name^=${filterName}]`).closest(filterDefaults.filterWrapperSelector);

      filter.classList.remove("filter-group");
      allFilters.querySelector(`[data-filter-name=${filterName}]`).appendChild(filter);
      selectedFilters.querySelector(`[data-filter-name=${filterName}]`).remove();

      let lookupGroup = selectedFilters.querySelector(`[data-filter-lookup=${filterName}]`);
      lookupGroup.classList.remove("filter-lookup--selected");
      lookupGroup.querySelector("select").selectedIndex = 0;
      allFilters.appendChild(lookupGroup);

      filterSelect.add(filterSelectInitialOptions.filter((el) => el.value === filterName)[0]);
      filterSelect.selectedIndex = 0;
    }
  });
});
