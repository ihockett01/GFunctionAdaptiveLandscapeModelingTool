import { ModelParameter } from "./model-parameter";
import { Wiki } from "./wiki";

export interface Model {
    id: string;
    value: string;
    parameters: Map<string, ModelParameter>;
    is3d: boolean;
    wiki: Wiki
}