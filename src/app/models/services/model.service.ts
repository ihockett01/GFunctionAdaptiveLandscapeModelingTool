import { HttpClient, HttpErrorResponse, HttpParams } from "@angular/common/http";
import {  Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { Model } from "../interfaces/model";
import { Injectable } from '@angular/core';
import { ModelParameter } from "../interfaces/model-parameter";


@Injectable({
  providedIn: 'root',
})
export class ModelService {
    
   private REST_API_SERVER = 'http://localhost:1400/api/';
   private MODELS_ENDPOINT = "models";
   private _model:Model;

    constructor(
      private httpClient: HttpClient) {
        //this.serverBootstrapper.createServer();
    }

    handleError(error: HttpErrorResponse) {
        let errorMessage = 'Unknown error!';
        if (error.error instanceof ErrorEvent) {
          // Client-side errors
          errorMessage = `Error: ${error.error.message}`;
        } else {
          // Server-side errors
          errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
        }
        
        return throwError(errorMessage);
      }

    public GetModelInformation():Observable<any> {
        console.log(this.REST_API_SERVER + this.MODELS_ENDPOINT);
        return this.httpClient
          .get(this.REST_API_SERVER + this.MODELS_ENDPOINT)
          .pipe(retry(3), catchError(this.handleError));
    }

    public GetChart():Observable<any>
    {
        //let argsAsJson = JSON.stringify(this._model.parameters);
        let params = new HttpParams();

        this._model.parameters.forEach((value: ModelParameter, key: string) => {
          params = params.append(value.id, JSON.stringify(value.value));
        });

        console.log(params);
        var endpoint = this.MODELS_ENDPOINT;
        console.log(this._model.is3d)
        if (this._model.is3d)
        {
          endpoint += '3d';
        }

        return this.httpClient
          .get(
            this.REST_API_SERVER + endpoint + '/' + this._model.id, 
            { params: params })
          .pipe(retry(3), catchError(this.handleError));
    }

    public ChangeModel(model:Model)
    {
        this._model = model;
    }

    public UpdateArgument(argumentName:string, value:object)
    {
        if (this._model.parameters.has(argumentName))
        {
          var modelParam = this._model.parameters.get(argumentName);
          modelParam.value = Number(value);
          this._model.parameters.set(argumentName, modelParam);
        }
    }

    public UpdateModelType(is3d)
    {
      console.log(is3d);
      console.log(is3d == "3d");
      this._model.is3d = is3d == "3d";
    }

    public ResetDefault()
    {
      this._model.parameters.forEach((value: ModelParameter, key: string) => {
        this.UpdateArgument(key, value.defaultValue);
      });
    }
}