/* eslint-disable */
/**
 * Engawa
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface LocationPublic
 */
export interface LocationPublic {
    /**
     * 
     * @type {string}
     * @memberof LocationPublic
     */
    path: string;
    /**
     * 
     * @type {number}
     * @memberof LocationPublic
     */
    id?: number | null;
}

/**
 * Check if a given object implements the LocationPublic interface.
 */
export function instanceOfLocationPublic(value: object): value is LocationPublic {
    if (!('path' in value) || value['path'] === undefined) return false;
    return true;
}

export function LocationPublicFromJSON(json: any): LocationPublic {
    return LocationPublicFromJSONTyped(json, false);
}

export function LocationPublicFromJSONTyped(json: any, ignoreDiscriminator: boolean): LocationPublic {
    if (json == null) {
        return json;
    }
    return {
        
        'path': json['path'],
        'id': json['id_'] == null ? undefined : json['id_'],
    };
}

  export function LocationPublicToJSON(json: any): LocationPublic {
      return LocationPublicToJSONTyped(json, false);
  }

  export function LocationPublicToJSONTyped(value?: LocationPublic | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'path': value['path'],
        'id_': value['id'],
    };
}

