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


/**
 * 
 * @export
 */
export const SubscriptionType = {
    Channel: 'Channel',
    Playlist: 'Playlist',
    Video: 'Video'
} as const;
export type SubscriptionType = typeof SubscriptionType[keyof typeof SubscriptionType];


export function instanceOfSubscriptionType(value: any): boolean {
    for (const key in SubscriptionType) {
        if (Object.prototype.hasOwnProperty.call(SubscriptionType, key)) {
            if (SubscriptionType[key as keyof typeof SubscriptionType] === value) {
                return true;
            }
        }
    }
    return false;
}

export function SubscriptionTypeFromJSON(json: any): SubscriptionType {
    return SubscriptionTypeFromJSONTyped(json, false);
}

export function SubscriptionTypeFromJSONTyped(json: any, ignoreDiscriminator: boolean): SubscriptionType {
    return json as SubscriptionType;
}

export function SubscriptionTypeToJSON(value?: SubscriptionType | null): any {
    return value as any;
}

export function SubscriptionTypeToJSONTyped(value: any, ignoreDiscriminator: boolean): SubscriptionType {
    return value as SubscriptionType;
}

