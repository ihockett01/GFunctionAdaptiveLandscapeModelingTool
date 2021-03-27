import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';

import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { faRecycle } from '@fortawesome/free-solid-svg-icons';
import { faInfo } from '@fortawesome/free-solid-svg-icons';

import { NgxSpinnerModule } from "ngx-spinner";

import { HomeRoutingModule } from './main-routing.module';

import { MainComponent } from './main.component';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { GraphComponent } from './components/graph/graph.component';
import { WikiComponent } from './components/wiki/wiki.component';

@NgModule({
  declarations: [MainComponent, GraphComponent, WikiComponent],
  imports: [
    CommonModule, 
    SharedModule, 
    HomeRoutingModule, 
    BrowserModule, 
    FormsModule, 
    ReactiveFormsModule,
    FontAwesomeModule,
    NgxSpinnerModule],
  providers: [],
  bootstrap:[MainComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MainModule {
  constructor(private library: FaIconLibrary)
  {
    this.library.addIcons(faPlay, faRecycle, faInfo);
  }

}
