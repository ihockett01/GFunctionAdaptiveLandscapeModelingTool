import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ModelService } from './services/model.service';
import { Subject } from 'rxjs';
import { NgxSpinnerService } from "ngx-spinner";
import { Model } from './interfaces/model';
import { ModelParameter } from './interfaces/model-parameter';




declare function drawDiagram(data: any): any;

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit, OnDestroy {

  destroy$: Subject<boolean> = new Subject<boolean>();

  public modelList: Map<string, object>;
  public parameterList: Map<string, ModelParameter>;
  public IsModelSelected: boolean;

  constructor(
    private router: Router, 
    private modelService: ModelService,
    private spinner: NgxSpinnerService) 
  { 
    
  }

  changeModel(e) {
    console.log(e.target.value);
    
    this.IsModelSelected = !e.target.diabled;
    console.log(this.IsModelSelected);

    if (!this.IsModelSelected) return;

    let selectedModel = this.modelList.get(e.target.value);
    this.parameterList = new Map<string, ModelParameter>();
    let parameters = JSON.parse(selectedModel['parameters']);

    console.log(parameters);
    
    let values = Object.values(parameters);

    for (var i = 0; i < values.length; i++) {
      let val : any = values[i];

      let modelParameter:ModelParameter = {
        id: val.ID,
        name: val.ObjectDescription,
        defaultValue: val.DefaultValue,
        value: val.DefaultValue,
        type: ''
      }
      this.parameterList.set(val.ID, modelParameter);
    }

    let model:Model = {
      id: selectedModel['id'],
      value: selectedModel['value'],
      parameters: this.parameterList,
      is3d: false,
      wiki: null
    };

    this.modelService.ChangeModel(model);
  }

  changeParameterValue(e) {
    let argumentName = e.target.name;
    let argumentValue = e.target.value;
    console.log(e);
    console.log(argumentName);
    console.log(argumentValue);
    this.modelService.UpdateArgument(argumentName, argumentValue);
  }

  changeModelType(e) {
    let argumentValue = e.target.value;
    this.modelService.UpdateModelType(argumentValue);
  }

  refreshGraph() : void {
    if (!this.IsModelSelected) return;
    
    console.log("loading figure");
    this.modelService.GetChart().subscribe((data: any) => {
      drawDiagram(data);
    });
  }

  resetDefault() {
    this.modelService.ResetDefault();
  }

  showWiki() {

  }

  ngOnInit(): void {
    this.modelService.GetModelInformation().subscribe((data: any)=>{
      this.modelList = new Map<string, object>();
      for (var i = 0; i < data.length; i++) {
        this.modelList.set(data[i].id, data[i]);
      }
      console.log(this.modelList);
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    // Unsubscribe from the subject
    this.destroy$.unsubscribe();
  }

}
