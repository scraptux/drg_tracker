<template>
<div class="w-full min-h-full bg-gray-800 flex flex-col">
  <div class="m-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center grow flex flex-col my-10">
    <div class="grow"></div>
    <div class="grow-0">
      <h1 class="mx-auto max-w-7xl font-display font-medium tracking-tight text-slate-100 text-3xl md:text-5xl pb-10">
        ICD-10-GM und OPS-Codes <br>
        <span class="relative whitespace-nowrap text-indigo-500">
          <svg aria-hidden="true" viewBox="0 0 418 42" class="absolute top-2/3 left-0 h-[0.58em] w-full fill-indigo-800/70" preserveAspectRatio="none"><path d="M203.371.916c-26.013-2.078-76.686 1.963-124.73 9.946L67.3 12.749C35.421 18.062 18.2 21.766 6.004 25.934 1.244 27.561.828 27.778.874 28.61c.07 1.214.828 1.121 9.595-1.176 9.072-2.377 17.15-3.92 39.246-7.496C123.565 7.986 157.869 4.492 195.942 5.046c7.461.108 19.25 1.696 19.17 2.582-.107 1.183-7.874 4.31-25.75 10.366-21.992 7.45-35.43 12.534-36.701 13.884-2.173 2.308-.202 4.407 4.442 4.734 2.654.187 3.263.157 15.593-.78 35.401-2.686 57.944-3.488 88.365-3.143 46.327.526 75.721 2.23 130.788 7.584 19.787 1.924 20.814 1.98 24.557 1.332l.066-.011c1.201-.203 1.53-1.825.399-2.335-2.911-1.31-4.893-1.604-22.048-3.261-57.509-5.556-87.871-7.36-132.059-7.842-23.239-.254-33.617-.116-50.627.674-11.629.54-42.371 2.494-46.696 2.967-2.359.259 8.133-3.625 26.504-9.81 23.239-7.825 27.934-10.149 28.304-14.005.417-4.348-3.529-6-16.878-7.066Z"></path></svg>
          <span class="relative">leicht und übersichtlich</span>
        </span>
        verfolgen.
      </h1>
      <p class="mx-auto mt-10 max-w-2xl text-lg tracking-tight text-slate-300">
        Finde deine ICD- und OPS-Codes und Unterschiede zwischen einzelnen Versionen.<br>
        Vermeide somit unbemerkte Fehler in der Auswertung von Patientendaten<br>
        durch Änderungen der Kodierung.
      </p>
      <div class="mt-6 flex justify-center gap-x-6">
        <router-link :to="`/icd/`" class="group inline-flex items-center justify-center rounded-full py-2 px-4 text-sm font-semibold focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 bg-slate-100 text-slate-800 hover:bg-slate-300 hover:text-slate-800 focus-visible:outline-slate-200">
          ICD-10-Codes
          <i class="fa-solid fa-chevron-right text-xs pl-2"></i>
        </router-link>
        <router-link :to="`/ops/`" class="group inline-flex items-center justify-center rounded-full py-2 px-4 text-sm font-semibold focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 bg-slate-100 text-slate-800 hover:bg-slate-300 hover:text-slate-800 focus-visible:outline-slate-200">
          OPS-Codes
          <i class="fa-solid fa-chevron-right text-xs pl-2"></i>
        </router-link>
      </div>
      <div class="relative mt-8 mb-3" style="height: 86px">
        <div class="absolute w-full h-full opacity-70">
          <div id="timeline-container">
            <svg viewBox="0 0 1460 190" style="max-height: 152px;" class="mx-auto"><g>
              <text x="130" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2010</text>
              <text x="230" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2011</text>
              <text x="330" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2012</text>
              <text x="430" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2013</text>
              <text x="530" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2014</text>
              <text x="630" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2015</text>
              <text x="730" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2016</text>
              <text x="830" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2017</text>
              <text x="930" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2018</text>
              <text x="1030" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2019</text>
              <text x="1130" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2020</text>
              <text x="1230" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2021</text>
              <text x="1330" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2022</text>
              <text x="1430" y="130" dy="50" font-weight="500" font-size="20" style="text-anchor: middle; fill: rgb(241, 245, 249);">2023</text>
              <path d="M130,130C180,130 80,130 1430,130" style="fill: none; stroke: #3730A3; stroke-width: 5px;"></path>
              <path d="M930,130C980,130 980,30 1030,30" style="fill: none; stroke: #3730A3; stroke-width: 5px;"></path>
              <path d="M1030,30C1080,30 1080,30 1430,30" style="fill: none; stroke: #3730A3; stroke-width: 5px;"></path>
              <g class="circle"><circle cx="130" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="130" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="230" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="230" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="330" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="330" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="430" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="430" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="530" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="530" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="630" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="630" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="730" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="730" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="830" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="830" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="930" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="930" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1030" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="1030" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1130" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="1130" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1230" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="1230" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1330" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="1330" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1430" cy="130" r="10" style="fill: #4F46E5;"></circle><text x="1430" y="130" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.8</text></g>
              <g class="circle"><circle cx="1030" cy="30" r="10" style="fill: #4F46E5;"></circle><text x="1030" y="30" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.3</text></g>
              <g class="circle"><circle cx="1130" cy="30" r="10" style="fill: #4F46E5;"></circle><text x="1130" y="30" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.3</text></g>
              <g class="circle"><circle cx="1230" cy="30" r="10" style="fill: #4F46E5;"></circle><text x="1230" y="30" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.3</text></g>
              <g class="circle"><circle cx="1330" cy="30" r="10" style="fill: #4F46E5;"></circle><text x="1330" y="30" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.3</text></g>
              <g class="circle"><circle cx="1430" cy="30" r="10" style="fill: #4F46E5;"></circle><text x="1430" y="30" dx="0" dy="-15" font-weight="300" style="text-anchor: middle; fill: rgb(203, 213, 225);">R00.3</text></g>
            </g></svg>
          </div>
        </div>
        <div class="absolute w-full h-full bg-gradient-to-l from-transparent to-gray-800"></div>
      </div>
    </div>
    <div class="grow"></div>
  </div>
  <div class="flex flex-col items-center border-t border-slate-400/10 py-6 sm:flex-row-reverse sm:justify-between mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 w-full">
    <div class="flex gap-x-6">
      <router-link :to="`/impressum/`" class="text-sm text-slate-500">Impressum</router-link>
      <a class="group" href="https://linkedin.com/in/thomas-jasny">
        <svg class="h-6 w-6 fill-slate-500 group-hover:fill-slate-700" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>
      </a>
      <a class="group" href="https://github.com/scraptux/drg_tracker">
        <svg class="h-6 w-6 fill-slate-500 group-hover:fill-slate-700" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>
      </a>
    </div>
    <p class="mt-6 text-sm text-slate-500 sm:mt-0">
      © 2024 Thomas Jasny. Alle Rechte vorbehalten.
    </p>
  </div>
</div>
</template>