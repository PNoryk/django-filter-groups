var t, ee;

document.addEventListener("DOMContentLoaded", () => {
  let selectedFilters = document.getElementById("selectedFilters");
  let allFilters = document.getElementById("allFiltersByGroups");

  let filterSelect = document.getElementById("id_filter");
  let filterSelectInitialOptions = [...filterSelect.options];
  filterSelect.addEventListener("change", (e) => {
    let selectedValue = e.target.selectedOptions[0].value;
    e.target.remove(e.target.selectedIndex);

    let selectedElements = {
      lookup: document.querySelector(`[data-filter-lookup=${selectedValue}]`),
      filters: document.querySelector(`[data-filter-name=${selectedValue}]`),
    };
    for (let el of Object.values(selectedElements)) {
      selectedFilters.appendChild(el);
    }
    selectedElements.lookup.classList.add("filter-lookup--selected");
  });

  document.querySelectorAll("[data-filter-lookup]").forEach((el) => {
    el.addEventListener("change", (e) => {
      let selectedValue = e.target.selectedOptions[0].value;
      let filterLookup = el.dataset.filterLookup;
      let allFiltersBlock = selectedFilters.querySelector(`[data-filter-name=${filterLookup}]`);
      if (selectedValue) {
        if (selectedValue === "exact") {
          selectedValue = "";
        }
        let selectedFilter = selectedFilters.querySelector(
          `[name=${[filterLookup, selectedValue].filter(Boolean).join("__")}`
        );
        let rowWithRemoveButton = document.createElement("div");
        rowWithRemoveButton.className = "filter";

        let group = selectedFilter.parentNode;
        group.classList.add("filter-group");

        let removeButton = document.createElement("button");
        removeButton.className = "filter-remove-btn";
        removeButton.type = "button";

        rowWithRemoveButton.appendChild(group);
        rowWithRemoveButton.appendChild(removeButton);

        let oldFilter = el.querySelector(".filter");
        if (oldFilter) {
          allFiltersBlock.appendChild(oldFilter.querySelector(".filter-group"));
          oldFilter.remove();
        }

        el.appendChild(rowWithRemoveButton);
      } else {
        let filter = el.querySelector(".filter");
        allFiltersBlock.appendChild(filter.querySelector(".filter-group"));
        filter.remove();
      }
    });
  });

  document.addEventListener("click", (e) => {
    let target = e.target;
    ee = e;
    t = target;
    if (target.classList.contains("filter-remove-btn")) {
      let filterLookupBlock = target.closest("[data-filter-lookup]");
      filterLookupBlock.classList.remove("filter-lookup--selected");

      let filterName = filterLookupBlock.dataset.filterLookup;

      let currentFilterFiltersBlock = document.querySelector(`[data-filter-name=${filterName}]`);
      let filter = target.closest(".filter");
      let filterGroup = filter.querySelector(".filter-group");
      filterGroup.classList.remove("filter-group");
      currentFilterFiltersBlock.appendChild(filterGroup);
      filter.remove();

      selectedFilters
        .querySelectorAll(`[data-filter-name=${filterName}], [data-filter-lookup=${filterName}]`)
        .forEach((el) => allFilters.appendChild(el));
      filterSelect.add(filterSelectInitialOptions.filter((el) => el.value === filterName)[0]);
    }
  });
});
